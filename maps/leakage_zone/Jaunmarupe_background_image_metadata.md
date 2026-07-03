# Jaunmarupe_background_image.tiff — Orthophoto Basemap

## Summary

| Property | Value |
|---|---|
| File | `Jaunmarupe_background_image.tiff` |
| Format | GeoTIFF |
| CRS | EPSG:3857 (WGS 84 / Web Mercator) |
| Resolution | 35.28 m/pixel |
| Size | 1616 × 792 pixels |
| Bands | 4 (RGBA) |
| Data type | uint8 |
| Coverage | ~31.2 × 15.3 km |
| File size | 4.5 MB |

## Bounding box (WGS 84)

| | Longitude | Latitude |
|---|---|---|
| West | 23.615910 | |
| East | 24.128029 | |
| South | | 56.771543 |
| North | | 56.908828 |

## Description

Low-resolution overview orthophoto covering the Jaunmārupe project area and its
surroundings, used as a basemap for all project maps. The image is a Web Mercator
(EPSG:3857) export of the LVM Ortofoto 7/8th cycle WMS service, captured at a
scale suited for regional overview mapping (1:75,000–1:100,000).

The 35 m/pixel resolution is intentionally coarse — this file is a basemap tile
for cartographic visualisation only, not for spatial analysis. High-resolution
LiDAR-derived products (DTM, CHM) at 1 m/pixel are stored separately in the
`05_analyses/Jaunmarupe_Bogwoodland_DTM/` and
`05_analyses/Jaunmarupe_Bogwoodland_CHM/` directories.

## Data source

LVM Ortofoto — 7th/8th cycle aerial orthophoto mosaic  
Latvijas Valsts meži (LVM) — Latvian State Forests  
Accessed via WMS: `https://lvmgeoserver.lvm.lv/geoserver/ows`  
Layer: `public:Orto_LKS`  
Licence: Open data (LVM open data terms)

## Usage in this project

Used as the basemap raster in:
- `05_analyses/jaunmarupe_surrounding_areas_map.py` — surrounding areas overview map
- `05_analyses/hydrology_map.py` — MKIS drainage network map
- `05_analyses/dtm_rewetting_map.py` — DTM rewetting potential map
- `05_analyses/digitize_peat_extraction.py` — peat extraction digitising tool

Also embedded in `05_analyses/outputs/jaunmarupe_overview_data.gpkg`
as the `ortofoto` raster layer for repository reviewers.
