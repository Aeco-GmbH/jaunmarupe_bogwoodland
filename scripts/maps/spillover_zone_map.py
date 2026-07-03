"""
Spillover zone map — Jaunmarupe project
Defines the 500 m buffer ring around the project boundary,
overlays on a basemap, and saves PNG, PDF and GeoPackage.
"""

import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import rasterio
from rasterio.plot import reshape_as_image

BASE = "[PATH]/01_projects/02_EU_LIFE_Biodiv_CrEW/05_PIN/01_Jaunmarupe/05_analyses/EUNIS_habitats"
os.makedirs(f"{BASE}/outputs", exist_ok=True)
BOUNDARY_FILE    = f"{BASE}/jaunmarupe_project_site.gpkg"
OUTPUT_GPKG      = f"{BASE}/outputs/leakage_zone_500m.gpkg"
OUTPUT_PNG       = f"{BASE}/outputs/leakage_zone_map.png"
OUTPUT_PDF       = f"{BASE}/outputs/leakage_zone_map.pdf"
ORTHO_FILE       = "/Users/amadotalita/Documents/01_projects/02_EU_LIFE_Biodiv_CrEW/05_PIN/01_Jaunmarupe/04_GIS/Jaunmarupe_background_image.tiff"
BUFFER_M         = 500

# ── Build geometries ──────────────────────────────────────────────────────────
boundary = gpd.read_file(BOUNDARY_FILE).to_crs(epsg=3035)
site_union = boundary.union_all()

# 500 m outer buffer
outer = site_union.buffer(BUFFER_M)

# Leakage zone = buffer ring (outer minus project site)
leakage_geom = outer.difference(site_union)

leakage_gdf = gpd.GeoDataFrame(
    [{"name": "Leakage zone (500 m)", "buffer_m": BUFFER_M,
      "geometry": leakage_geom}],
    crs="EPSG:3035"
)

# Save GeoPackage (leakage zone + project boundary as separate layers)
leakage_gdf.to_file(OUTPUT_GPKG, layer="leakage_zone", driver="GPKG")
boundary.to_file(OUTPUT_GPKG, layer="project_boundary", driver="GPKG")
print(f"GeoPackage saved → {OUTPUT_GPKG}")

area_ha = leakage_gdf.geometry.area.sum() / 10_000
print(f"Leakage zone area: {area_ha:.1f} ha")

# ── Reproject to Web Mercator for basemap ─────────────────────────────────────
boundary_wm  = boundary.to_crs(epsg=3857)
leakage_wm   = leakage_gdf.to_crs(epsg=3857)

# Plot extent: outer buffer + extra margin for context
bounds       = leakage_wm.total_bounds          # (xmin, ymin, xmax, ymax)
margin       = 800
xmin, ymin   = bounds[0] - margin, bounds[1] - margin
xmax, ymax   = bounds[2] + margin, bounds[3] + margin

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 12))
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# Orthophoto basemap from local TIFF
with rasterio.open(ORTHO_FILE) as src:
    img_data = src.read()                   # (bands, rows, cols)
    img_extent = [src.bounds.left, src.bounds.right,
                  src.bounds.bottom, src.bounds.top]
# Use RGB (first 3 bands); normalise to 0-1 for imshow
rgb = reshape_as_image(img_data[:3]).astype(np.float32) / 255.0
ax.imshow(rgb, extent=img_extent, origin="upper",
          interpolation="bilinear", zorder=0)

# Leakage zone — semi-transparent orange fill
leakage_wm.plot(ax=ax, color="#F4A44A", alpha=0.45,
                edgecolor="#D4730A", linewidth=1.0, zorder=2)

# Project boundary — red outline only, no fill
boundary_wm.plot(ax=ax, color="none",
                 edgecolor="#CC0000", linewidth=2.0, zorder=3)

# ── Scale bar (1 km) ─────────────────────────────────────────────────────────
sb_x  = xmin + (xmax - xmin) * 0.05
sb_y  = ymin + (ymax - ymin) * 0.04
sb_len = 1000
ax.plot([sb_x, sb_x + sb_len], [sb_y, sb_y],
        color="white", linewidth=4, zorder=6, solid_capstyle="butt")
ax.plot([sb_x, sb_x + sb_len], [sb_y, sb_y],
        color="black", linewidth=2, zorder=7, solid_capstyle="butt")
for tick_x in [sb_x, sb_x + sb_len]:
    ax.plot([tick_x, tick_x], [sb_y - 60, sb_y + 60],
            color="black", linewidth=1.5, zorder=7)
ax.text(sb_x + sb_len / 2, sb_y + 120, "1 km",
        ha="center", va="bottom", fontsize=8, zorder=7,
        path_effects=[pe.withStroke(linewidth=2, foreground="white")])

# ── North arrow (top-left, filled triangle style like reference image) ─────────
from matplotlib.patches import FancyArrowPatch, Polygon as MplPolygon
na_x = xmin + (xmax - xmin) * 0.06
na_y = ymax - (ymax - ymin) * 0.08
arrow_len = (ymax - ymin) * 0.055
hw = arrow_len * 0.35   # half-width of triangle base

# Filled black upward-pointing triangle
triangle = MplPolygon(
    [[na_x, na_y + arrow_len],
     [na_x - hw, na_y],
     [na_x + hw, na_y]],
    closed=True, facecolor="black", edgecolor="black", zorder=8
)
ax.add_patch(triangle)
ax.text(na_x, na_y + arrow_len + (ymax - ymin) * 0.012, "N",
        ha="center", va="bottom", fontsize=11, fontweight="bold",
        color="black", zorder=8,
        path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])

# ── Legend ────────────────────────────────────────────────────────────────────
from matplotlib.lines import Line2D
legend_items = [
    Line2D([0], [0], color="#CC0000", linewidth=2.0, label="Project boundary"),
    mpatches.Patch(facecolor="#F4A44A", alpha=0.6,
                   edgecolor="#D4730A", linewidth=1.0,
                   label=f"Leakage zone ({BUFFER_M} m buffer, {area_ha:.0f} ha)"),
]
ax.legend(handles=legend_items, loc="lower right", fontsize=9,
          framealpha=0.9, edgecolor="#AAAAAA")

ax.set_title(
    "Leakage Zone — Jaunmarupe Project Area\n"
    "500 m external buffer · Basemap: LVM Ortofoto (EPSG:3857)",
    fontsize=11, pad=12,
)
ax.set_axis_off()

plt.tight_layout()
fig.savefig(OUTPUT_PNG, dpi=200, bbox_inches="tight")
print(f"Map saved → {OUTPUT_PNG}")
fig.savefig(OUTPUT_PDF, bbox_inches="tight")
print(f"Map saved → {OUTPUT_PDF}")
plt.close()
print("Done.")
