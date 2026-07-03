"""
dtm_rewetting_map.py — Jaunmarupe project
Rewetting potential map: DTM microtopography + drainage network overlay.

Shows:
  - Orthophoto basemap (full coverage)
  - DTM elevation colour ramp + hillshade (semi-transparent, drapes over ortho)
  - Rewetting potential zones clipped to project boundary
  - Drain collectors, ditches, drainpipes from MKIS
  - Drain collector × project boundary crossing points (candidate blocking sites)
  - Project boundary

Output:
  outputs/jaunmarupe_dtm_rewetting.png
  outputs/jaunmarupe_dtm_rewetting.pdf
"""

import os
import glob
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.colors import LinearSegmentedColormap
import rasterio
from rasterio.merge import merge
from rasterio.crs import CRS
from rasterio.transform import from_bounds as rt_from_bounds
from rasterio.features import geometry_mask
from scipy.ndimage import uniform_filter, binary_dilation
from shapely.geometry import MultiPoint, Point
from shapely.ops import unary_union
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE     = "[PATH]/01_projects/02_EU_LIFE_Biodiv_CrEW/05_PIN/01_Jaunmarupe/05_analyses"
GDB      = f"{BASE}/MKIS_20180612.gdb"
BOUNDARY = f"{BASE}/EUNIS_habitats/jaunmarupe_project_site.gpkg"
DTM_DIR  = f"{BASE}/Jaunmarupe_Bogwoodland_DTM"
OUT_DIR  = f"{BASE}/outputs"
os.makedirs(OUT_DIR, exist_ok=True)

OUTPUT_PNG = f"{OUT_DIR}/jaunmarupe_dtm_rewetting.png"
OUTPUT_PDF = f"{OUT_DIR}/jaunmarupe_dtm_rewetting.pdf"

# ── 1. Load project boundary ──────────────────────────────────────────────────
print("Loading boundary …")
boundary    = gpd.read_file(BOUNDARY).to_crs(epsg=3059)
boundary_wm = boundary.to_crs(epsg=3857)

# ── 2. Mosaic DTM tiles ────────────────────────────────────────────────────────
print("Mosaicking DTM tiles …")
dtm_files = sorted(glob.glob(f"{DTM_DIR}/*.tif"))
datasets  = [rasterio.open(f) for f in dtm_files]
mosaic, mosaic_transform = merge(datasets, nodata=-9999.0)
for ds in datasets:
    ds.close()

dtm = mosaic[0].astype(np.float32)
dtm[dtm == -9999.0] = np.nan

# Clip DTM to ROI in EPSG:3059
bnd_3059 = boundary.total_bounds
r_buf = 700
roi_xmin = bnd_3059[0] - r_buf; roi_ymin = bnd_3059[1] - r_buf
roi_xmax = bnd_3059[2] + r_buf; roi_ymax = bnd_3059[3] + r_buf

rows0 = max(int((mosaic_transform.f - roi_ymax) / (-mosaic_transform.e)), 0)
rows1 = min(int((mosaic_transform.f - roi_ymin) / (-mosaic_transform.e)), dtm.shape[0])
cols0 = max(int((roi_xmin - mosaic_transform.c) / mosaic_transform.a), 0)
cols1 = min(int((roi_xmax - mosaic_transform.c) / mosaic_transform.a), dtm.shape[1])

dtm_clip = dtm[rows0:rows1, cols0:cols1]
clip_left   = mosaic_transform.c + cols0 * mosaic_transform.a
clip_top    = mosaic_transform.f + rows0 * mosaic_transform.e
clip_right  = mosaic_transform.c + cols1 * mosaic_transform.a
clip_bottom = mosaic_transform.f + rows1 * mosaic_transform.e

print(f"  DTM clip shape: {dtm_clip.shape}")
print(f"  Elevation range: {np.nanmin(dtm_clip):.2f} – {np.nanmax(dtm_clip):.2f} m")

# ── 4. Reproject DTM extent corners to EPSG:3857 for imshow extent ────────────
# Use pyproj to transform the four corners
from pyproj import Transformer
t = Transformer.from_crs(3059, 3857, always_xy=True)
dtm_left_wm,  dtm_bottom_wm = t.transform(clip_left,  clip_bottom)
dtm_right_wm, dtm_top_wm    = t.transform(clip_right, clip_top)
dtm_img_ext = [dtm_left_wm, dtm_right_wm, dtm_bottom_wm, dtm_top_wm]

# Map display extent (Web Mercator) matches DTM coverage
px_min, py_min = dtm_left_wm,  dtm_bottom_wm
px_max, py_max = dtm_right_wm, dtm_top_wm

# ── 5. Hillshade ──────────────────────────────────────────────────────────────
print("Computing hillshade …")
def hillshade(dem, azimuth=315, altitude=35, res=1.0):
    az_rad  = np.radians(360 - azimuth + 90)
    alt_rad = np.radians(altitude)
    dy, dx  = np.gradient(dem, res)
    slope   = np.arctan(np.sqrt(dx**2 + dy**2))
    aspect  = np.arctan2(-dy, dx)
    hs = (np.sin(alt_rad) * np.cos(slope)
          + np.cos(alt_rad) * np.sin(slope) * np.cos(az_rad - aspect))
    return np.clip(hs, 0, 1)

dtm_filled_hs = np.where(np.isnan(dtm_clip), np.nanmean(dtm_clip), dtm_clip)
hs = hillshade(dtm_filled_hs)

# ── 6. Rewetting potential zones (inside boundary only) ───────────────────────
print("Computing rewetting potential zones …")
dtm_smooth   = uniform_filter(dtm_filled_hs, size=400)
relative_low = (dtm_clip - dtm_smooth) <= 0.3

clip_h, clip_w = dtm_clip.shape
clip_transform = rt_from_bounds(clip_left, clip_bottom, clip_right, clip_top,
                                clip_w, clip_h)
boundary_mask = geometry_mask(
    [geom.__geo_interface__ for geom in boundary.geometry],
    out_shape=(clip_h, clip_w),
    transform=clip_transform,
    invert=True)

rewet_zone = relative_low & boundary_mask & ~np.isnan(dtm_clip)

# ── 7. Load hydrology layers ──────────────────────────────────────────────────
print("Loading hydrology layers …")
bbox_3059 = (roi_xmin, roi_ymin, roi_xmax, roi_ymax)
collectors = gpd.read_file(GDB, layer="DrainCollectors", engine="pyogrio", bbox=bbox_3059)
ditches    = gpd.read_file(GDB, layer="Ditches",         engine="pyogrio", bbox=bbox_3059)
drainpipes = gpd.read_file(GDB, layer="Drainpipes",      engine="pyogrio", bbox=bbox_3059)
print(f"  Collectors: {len(collectors)}, Ditches: {len(ditches)}, Drainpipes: {len(drainpipes)}")

collectors_wm = collectors.to_crs(epsg=3857)
ditches_wm    = ditches.to_crs(epsg=3857)
drainpipes_wm = drainpipes.to_crs(epsg=3857)

# ── 8. Drain collector × boundary crossing points ─────────────────────────────
print("Computing drain collector crossing points …")
boundary_line = boundary_wm.geometry.boundary.unary_union   # exterior ring(s)
crossing_pts  = []
for geom in collectors_wm.geometry:
    inter = geom.intersection(boundary_line)
    if inter.is_empty:
        continue
    if inter.geom_type == "Point":
        crossing_pts.append(inter)
    elif inter.geom_type == "MultiPoint":
        crossing_pts.extend(list(inter.geoms))
    elif inter.geom_type in ("GeometryCollection", "MultiLineString"):
        for g in inter.geoms:
            if g.geom_type == "Point":
                crossing_pts.append(g)

print(f"  Crossing points found: {len(crossing_pts)}")
if crossing_pts:
    crossing_gdf = gpd.GeoDataFrame(
        geometry=crossing_pts, crs="EPSG:3857")

# ── 9. Plot ───────────────────────────────────────────────────────────────────
print("Plotting …")
fig, ax = plt.subplots(figsize=(13, 12))
ax.set_xlim(px_min, px_max)
ax.set_ylim(py_min, py_max)
ax.set_aspect("equal")
ax.set_facecolor("#dde3e8")   # neutral blue-grey for nodata areas

# DTM colour ramp — opaque where tiles exist, transparent where nodata
elev_min = np.nanpercentile(dtm_clip, 2)
elev_max = np.nanpercentile(dtm_clip, 98)
peat_colors = [
    (0.00, "#1a4a6b"),
    (0.10, "#2e7aa6"),
    (0.25, "#5aaa8e"),
    (0.42, "#9ac878"),
    (0.58, "#d4c97e"),
    (0.74, "#c4a96e"),
    (0.88, "#b8926a"),
    (1.00, "#e8d5b0"),
]
cmap_elev = LinearSegmentedColormap.from_list(
    "peat_terrain", [(v, c) for v, c in peat_colors])

nodata_mask = np.isnan(dtm_clip)
dtm_norm = np.clip((np.nan_to_num(dtm_clip, nan=elev_min) - elev_min)
                   / (elev_max - elev_min), 0, 1)
dtm_rgba = cmap_elev(dtm_norm)
dtm_rgba[..., 3] = np.where(nodata_mask, 0.0, 1.0)
ax.imshow(dtm_rgba, extent=dtm_img_ext, origin="upper",
          interpolation="bilinear", zorder=1)

# Hillshade overlay — also transparent where nodata
hs_rgba = np.zeros((*hs.shape, 4), dtype=np.float32)
hs_rgba[..., :3] = hs[..., np.newaxis]
hs_rgba[..., 3]  = np.where(nodata_mask, 0.0, 0.28)
ax.imshow(hs_rgba, extent=dtm_img_ext, origin="upper",
          interpolation="bilinear", zorder=2)

# Rewetting potential zones (cyan, inside boundary only)
rewet_rgba = np.zeros((*rewet_zone.shape, 4), dtype=np.float32)
rewet_rgba[rewet_zone, 0] = 0.12
rewet_rgba[rewet_zone, 1] = 0.60
rewet_rgba[rewet_zone, 2] = 0.85
rewet_rgba[rewet_zone, 3] = 0.55
ax.imshow(rewet_rgba, extent=dtm_img_ext, origin="upper",
          interpolation="none", zorder=3)

# Drainpipes (grey, thin)
if len(drainpipes_wm):
    drainpipes_wm.plot(ax=ax, color="#888888", linewidth=0.4, alpha=0.70, zorder=4)

# Ditches (blue)
if len(ditches_wm):
    ditches_wm.plot(ax=ax, color="#1976D2", linewidth=0.9, alpha=0.90, zorder=5)

# Drain collectors (orange)
if len(collectors_wm):
    collectors_wm.plot(ax=ax, color="#E65100", linewidth=1.5, alpha=1.0, zorder=6)

# Project boundary
boundary_wm.plot(ax=ax, color="none", edgecolor="#CC0000",
                 linewidth=2.2, linestyle="--", zorder=7)

# Crossing points — candidate drain-blocking locations
if crossing_pts:
    # White halo + filled circle
    xs = [p.x for p in crossing_pts]
    ys = [p.y for p in crossing_pts]
    ax.scatter(xs, ys, s=120, color="white",   zorder=9, linewidths=0)
    ax.scatter(xs, ys, s=60,  color="#FFD600", zorder=10,
               edgecolors="#333333", linewidths=0.8)

# ── 10. Colour bar ────────────────────────────────────────────────────────────
import matplotlib.cm as mcm
import matplotlib.colors as mcolors2
sm = mcm.ScalarMappable(cmap=cmap_elev,
                        norm=mcolors2.Normalize(vmin=elev_min, vmax=elev_max))
sm.set_array([])
cax = inset_axes(ax, width="2.5%", height="32%",
                 loc="lower right", borderpad=1.8)
cb = fig.colorbar(sm, cax=cax)
cb.set_label("Elevation (m a.s.l.)", fontsize=7.5)
cb.ax.tick_params(labelsize=7)

# ── 11. Scale bar (1 km) ──────────────────────────────────────────────────────
sb_x = px_min + (px_max - px_min) * 0.05
sb_y = py_min + (py_max - py_min) * 0.04
sb_len = 1000
for col, lw in [("white", 5), ("black", 2.5)]:
    ax.plot([sb_x, sb_x + sb_len], [sb_y, sb_y],
            color=col, linewidth=lw, zorder=11, solid_capstyle="butt")
for tx in [sb_x, sb_x + sb_len]:
    ax.plot([tx, tx], [sb_y - 80, sb_y + 80],
            color="black", linewidth=1.5, zorder=11)
ax.text(sb_x + sb_len / 2, sb_y + 160, "1 km",
        ha="center", va="bottom", fontsize=8, zorder=11,
        path_effects=[pe.withStroke(linewidth=2, foreground="white")])

# ── 12. North arrow ───────────────────────────────────────────────────────────
na_x      = px_min + (px_max - px_min) * 0.07
na_y      = py_max - (py_max - py_min) * 0.09
arrow_len = (py_max - py_min) * 0.055
hw        = arrow_len * 0.35
triangle  = MplPolygon(
    [[na_x, na_y + arrow_len], [na_x - hw, na_y], [na_x + hw, na_y]],
    closed=True, facecolor="black", edgecolor="black", zorder=12)
ax.add_patch(triangle)
ax.text(na_x, na_y + arrow_len + (py_max - py_min) * 0.012, "N",
        ha="center", va="bottom", fontsize=11, fontweight="bold",
        color="black", zorder=12,
        path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])

# ── 13. Legend ────────────────────────────────────────────────────────────────
n_cross = len(crossing_pts)
rewet_patch = mpatches.Patch(
    facecolor="#1F99D9", alpha=0.65, edgecolor="#1565C0", linewidth=0.6,
    label="Rewetting potential zone\n(≤ 30 cm below local mean elevation)")
crossing_marker = Line2D([0], [0], marker="o", color="none",
                         markerfacecolor="#FFD600", markeredgecolor="#333333",
                         markeredgewidth=0.8, markersize=8,
                         label=f"Candidate drain-blocking point (n={n_cross})")
legend_items = [
    rewet_patch,
    crossing_marker,
    Line2D([0], [0], color="#CC0000", linewidth=2.0, linestyle="--",
           label="Project boundary"),
    Line2D([0], [0], color="#E65100", linewidth=1.8,
           label="Drain collector"),
    Line2D([0], [0], color="#1976D2", linewidth=1.0,
           label="Ditch"),
    Line2D([0], [0], color="#888888", linewidth=0.7,
           label="Drainpipe (subsurface)"),
]
leg = ax.legend(handles=legend_items, loc="lower left", fontsize=8.5,
                framealpha=1.0, facecolor="white", edgecolor="#888888",
                borderpad=0.9, labelspacing=0.55,
                title="Sources: LĢIA LiDAR DTM · MKIS (2018)",
                title_fontsize=7.5)
leg.get_frame().set_linewidth(0.8)

ax.set_title(
    "Microtopography and Rewetting Potential — Jaunmarupe Project Site\n"
    "DTM hillshade · Topographic low zones · MKIS drainage network · Candidate blocking points",
    fontsize=10, pad=12)
ax.set_axis_off()
plt.tight_layout()

fig.savefig(OUTPUT_PNG, dpi=200, bbox_inches="tight")
print(f"PNG → {OUTPUT_PNG}")
fig.savefig(OUTPUT_PDF, bbox_inches="tight")
print(f"PDF → {OUTPUT_PDF}")
plt.close()
print("Done.")
