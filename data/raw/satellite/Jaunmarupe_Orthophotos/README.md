# Jaunmarupe_Orthophotos — Temporal Orthophoto Comparison

## Summary

| Property | Value |
|---|---|
| Format | PNG (QGIS map export, non-georeferenced) |
| Files | 6 |
| Time periods | 2016, 2019/2020, 2022/2023 |
| Areas | Two sub-areas of the project site (Jaunmarupe, Jaunmarupe2) |
| Scale | 1:12,500 |
| CRS (source) | EPSG:3059 (LKS92 / Latvia TM) |

## Files

| File | Area | Period | Size |
|---|---|---|---|
| `Jaunmarupe_2016.png` | Western peat extraction area | 2016 | 1445 × 853 px |
| `Jaunmarupe 2019_2020.png` | Western peat extraction area | 2019/2020 | 1448 × 855 px |
| `Jaunmarupe_2022_2023.png` | Western peat extraction area | 2022/2023 | 1411 × 855 px |
| `Jaunmarupe2 2016.png` | Eastern peat extraction area | 2016 | 1442 × 855 px |
| `Jaunmarupe2_2019_2020.png` | Eastern peat extraction area | 2019/2020 | 1438 × 853 px |
| `Jaunmarupe2_2022_2023.png` | Eastern peat extraction area | 2022/2023 | 1440 × 857 px |

## Description

Six QGIS map exports showing the temporal evolution of active peat extraction
within the Jaunmārupe project area across three orthophoto cycles. Each image
covers the same spatial extent at 1:12,500 scale, allowing direct visual
comparison of land cover change over approximately seven years.

Two sub-areas are documented:
- **Jaunmarupe** — western portion of the project boundary, covering the main
  peat extraction block to the west and centre.
- **Jaunmarupe2** — eastern portion, covering the peat extraction areas to the
  east of the main bog.

### Overlaid layers (from QGIS)
- **Pink / magenta hatched polygons** — active peat extraction areas
- **Green outline** — Jaunmārupe project boundary

### Orthophoto cycles
| Period | LVM cycle | Notes |
|---|---|---|
| 2016 | 5th cycle | Greyscale imagery; baseline state |
| 2019/2020 | 6th cycle | Colour imagery; intermediate state |
| 2022/2023 | 7th/8th cycle | Colour imagery; most recent state |

## Purpose

These images were produced to document the **progression of peat extraction**
within and adjacent to the project boundary as evidence for:

- The baseline degradation assessment in the biodiversity credit application
- Visual justification for active peat extraction polygons
  (`04_GIS/01_polygons/active_peat_extraction.gpkg`)
- Demonstrating ongoing threat and additionality of restoration intervention

## Important note

These are **non-georeferenced PNG screenshots** exported from QGIS, intended
for visual reference and document illustration only. They are not suitable for
spatial analysis. The underlying georeferenced orthophoto data is available via
the LVM WMS service:
`https://lvmgeoserver.lvm.lv/geoserver/ows`
Layer: `public:Orto_LKS`

## Data source

LVM Ortofoto — Latvijas Valsts meži (LVM) open data WMS service.  
Accessed and exported from QGIS by aeco GmbH.
