"""
jaunmarupe_surrounding_areas_map.py — Jaunmarupe project
Produces the surrounding-areas overview map for the Jaunmārupe biodiversity
credit application.

Layers displayed:
  - LVM Ortofoto basemap (EPSG:3857)
  - Jaunmārupe project boundary     (red outline)
  - Cenas Tīrelis Natura 2000       (green outline)
  - Melnā ezera purvs Natura 2000   (yellow outline)
  - Active peat extraction sites    (pink fill)

Map elements: north arrow, 3 km scale bar (3 × 1 km divisions).
Scale: 1:75,000.  No legend or title panel — use project_frame.png as overlay.

Outputs:
  outputs/jaunmarupe_surrounding_areas_map.png  (200 DPI)
  outputs/jaunmarupe_surrounding_areas_map.pdf
"""

import math
import os
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.plot import reshape_as_image
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE    = "[PATH]/01_projects/02_EU_LIFE_Biodiv_CrEW/05_PIN/01_Jaunmarupe"
ORTHO   = f"{BASE}/04_GIS/Jaunmarupe_background_image.tiff"
PROJ    = f"{BASE}/04_GIS/01_polygons/Jaunmarupe_Project_Latvia.gpkg"
CT      = f"{BASE}/04_GIS/01_polygons/cenas_tirelis_official.gpkg"
MEP     = f"{BASE}/04_GIS/01_polygons/melna_ezera_purvs.gpkg"
PEAT    = f"{BASE}/04_GIS/01_polygons/active_peat_extraction.gpkg"
OUT_DIR = f"{BASE}/05_analyses/outputs"
os.makedirs(OUT_DIR, exist_ok=True)

OUT_PNG = f"{OUT_DIR}/jaunmarupe_surrounding_areas_map.png"
OUT_PDF = f"{OUT_DIR}/jaunmarupe_surrounding_areas_map.pdf"

# ── Layer colours ──────────────────────────────────────────────────────────────
C_PROJ   = "#e41a1c"   # red
C_CT     = "#8ed749"   # green
C_MEP    = "#f0e442"   # yellow
C_PEAT_F = "#ff69b4"   # pink fill
C_PEAT_E = "#cc1177"   # pink edge

# ── Load layers (EPSG:3857 — matches orthophoto) ──────────────────────────────
print("Loading layers …")
proj_wm = gpd.read_file(PROJ).to_crs(3857)
ct_wm   = gpd.read_file(CT).to_crs(3857)
mep_wm  = gpd.read_file(MEP).to_crs(3857)
peat_wm = gpd.read_file(PEAT).to_crs(3857)

# ── Map extent: union of all layer bounds + 1800 m buffer ────────────────────
buf   = 1800
all_b = np.vstack([proj_wm.total_bounds, ct_wm.total_bounds,
                   mep_wm.total_bounds,  peat_wm.total_bounds])
xmin  = all_b[:, 0].min() - buf
xmax  = all_b[:, 2].max() + buf
ymin  = all_b[:, 1].min() - buf
ymax  = all_b[:, 3].max() + buf
map_w = xmax - xmin
map_h = ymax - ymin

# ── Figure size derived from 1:75,000 scale ───────────────────────────────────
cy      = (ymin + ymax) / 2
lat_deg = math.degrees(2 * math.atan(math.exp(cy / 6378137)) - math.pi / 2)
cos_lat = math.cos(math.radians(lat_deg))
true_w  = map_w * cos_lat   # true E–W ground distance in metres
true_h  = map_h * cos_lat

TARGET_SCALE = 75_000
fig_w_in = (true_w / TARGET_SCALE) / 0.0254
fig_h_in = (true_h / TARGET_SCALE) / 0.0254
print(f"Figure: {fig_w_in:.2f} × {fig_h_in:.2f} in  |  scale 1:{TARGET_SCALE:,}")

# ── Figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(fig_w_in, fig_h_in), facecolor="white")
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect("equal")
ax.set_axis_off()

# ── Orthophoto basemap ────────────────────────────────────────────────────────
with rasterio.open(ORTHO) as src:
    img     = reshape_as_image(src.read()[:3]).astype(np.float32) / 255.0
    img_ext = [src.bounds.left, src.bounds.right,
               src.bounds.bottom, src.bounds.top]
ax.imshow(img, extent=img_ext, origin="upper", interpolation="bilinear", zorder=0)

# ── Vector layers ─────────────────────────────────────────────────────────────
peat_wm.plot(ax=ax, facecolor=C_PEAT_F, edgecolor=C_PEAT_E,
             alpha=0.55, linewidth=1.2, zorder=2)
ct_wm.plot(ax=ax,   facecolor="none", edgecolor=C_CT,   linewidth=2.0, zorder=3)
mep_wm.plot(ax=ax,  facecolor="none", edgecolor=C_MEP,  linewidth=2.0, zorder=3)
proj_wm.plot(ax=ax, facecolor="none", edgecolor=C_PROJ, linewidth=2.5, zorder=4)

# ── Scale bar — 3 × 1 km alternating segments (bottom-left) ──────────────────
div_mu = 1_000 / cos_lat   # 1 km in Web Mercator units
sb_x0  = xmin + map_w * 0.04
sb_y   = ymin + map_h * 0.05
bar_h  = map_h * 0.012

for i, col in enumerate(["black", "white", "black"]):
    ax.add_patch(mpatches.Rectangle(
        (sb_x0 + i * div_mu, sb_y - bar_h / 2), div_mu, bar_h,
        facecolor=col, edgecolor="black", linewidth=0.8, zorder=6,
    ))
for i, lbl in enumerate(["0", "1", "2", "3 km"]):
    ax.text(
        sb_x0 + i * div_mu, sb_y - bar_h * 1.6,
        lbl, ha="center", fontsize=7.5, color="white", zorder=6,
        path_effects=[pe.withStroke(linewidth=2, foreground="black")],
    )

# ── North arrow (top-left) ────────────────────────────────────────────────────
na_x    = xmin + map_w * 0.05
na_y    = ymax - map_h * 0.07
arr_len = map_h * 0.05

ax.annotate("", xy=(na_x, na_y), xytext=(na_x, na_y - arr_len),
            arrowprops=dict(arrowstyle="->", color="white", lw=2.0), zorder=6)
ax.text(na_x, na_y + map_h * 0.012, "N",
        ha="center", va="bottom", fontsize=12, fontweight="bold",
        color="white", zorder=6,
        path_effects=[pe.withStroke(linewidth=2.5, foreground="black")])

# ── Save ──────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0)
plt.savefig(OUT_PNG, dpi=200, bbox_inches="tight", facecolor="white")
plt.savefig(OUT_PDF, bbox_inches="tight", facecolor="white")
plt.close()
print(f"Saved: {OUT_PNG}")
print(f"Saved: {OUT_PDF}")
