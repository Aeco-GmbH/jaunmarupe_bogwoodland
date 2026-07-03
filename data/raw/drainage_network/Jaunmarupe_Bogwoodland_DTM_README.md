# Jaunmarupe Bogwoodland — Digital Terrain Model (DTM)

> **Note for repository reviewers:** The `.tif` tile files are excluded from this
> repository due to their size (142 MB total). Download the tiles from the
> **LĢIA open data portal**: https://www.lgia.gov.lv/lv/dati — select
> *Lidar DTM 1m* and download the tiles listed in the tile naming section below.
> Place the downloaded files in this folder before running any analysis scripts.

## What this dataset is

A Digital Terrain Model (DTM) derived from airborne LiDAR, representing the elevation of the bare ground surface above mean sea level in metres. LiDAR ground returns are filtered to remove vegetation and buildings, producing a model of the underlying terrain. This is sometimes called a "bare-earth" model.

The dataset covers approximately 10 × 9 km around the Jaunmarupe project site in Latvia and is tiled following the Latvian national LiDAR grid.

## Technical specifications

| Property | Value |
|---|---|
| Format | GeoTIFF, Cloud-Optimised (COG) |
| CRS | EPSG:3059 (LKS92 / Latvia TM) |
| Resolution | 1 m/pixel |
| Tile size | ~1 × 1 km (1001 × 1001 pixels) |
| Number of tiles | 44 |
| Total coverage | ~90 km² |
| Data type | Float32 |
| NoData value | −9999.0 |
| Value range | 6.02 m – 19.49 m (above sea level) |
| Mean elevation | ~9.7 m a.s.l. (across all tiles) |

## Tile naming convention

Tiles are named after the Latvian national map grid cell code, e.g.:

```
3244-54-24_DTM_COG.tif
```

The numeric code (`3244-54-24`) identifies the 1 km × 1 km grid cell in the LKS92 coordinate system. The suffix `DTM_COG` indicates Digital Terrain Model in Cloud-Optimised GeoTIFF format.

## Likely data source

Latvian Geospatial Information Agency (LĢIA) national LiDAR survey. LĢIA provides open LiDAR products (DTM, DSM, CHM) at 1 m resolution under an open government data licence. Tiles are available via the LĢIA geoportal.

## Interpretation

The Jaunmarupe area is a low-lying landscape in central Latvia. The relatively narrow elevation range (6–19.5 m a.s.l.) is characteristic of the flat to gently undulating glaciofluvial and lacustrine deposits that underlie most of the Latvian lowlands. Within this range, microtopographic variation at the 0.1–1 m scale is ecologically highly significant for peatland hydrology:

- **Depressions and hollows** (local lows): areas of water accumulation, likely to support the wettest bog communities (Sphagnum pools, Rhynchospora spp.).
- **Hummocks and ridges** (local highs): slightly drier microsites, typically supporting Calluna, Eriophorum vaginatum, or Pinus sylvestris in bog woodland contexts.
- **Drainage gradients**: subtle slopes guide the direction of surface and subsurface water flow, determining where blocking drainage channels would have the greatest rewetting effect.

## Relevance to the Jaunmarupe biodiversity credit project

The DTM is the foundational spatial layer for hydrological analysis and restoration planning:

- **Topographic wetness index (TWI)**: computed from slope and flow accumulation derived from the DTM, TWI predicts where water naturally accumulates and where the water table is likely to be closest to the surface.
- **Rewetting modelling**: by simulating the effect of blocking or infilling drain collector outlets (see `../MKIS_20180612.gdb`), the DTM can be used to estimate how far a raised water table would extend across the bog, providing a spatial basis for additionality claims.
- **Microtopographic habitat mapping**: fine-scale elevation variation at the 1 m scale can distinguish hummock–hollow patterning characteristic of active raised bog (EUNIS Q11 / Natura 2000 7110) from flatter, degraded surfaces.
- **Subsidence monitoring baseline**: in peatlands under drainage pressure, peat oxidation causes measurable surface subsidence over years to decades. The current DTM provides a baseline against which future LiDAR surveys can be compared to quantify peat loss or recovery.

## Associated dataset

A paired Canopy Height Model (CHM) is stored in `../Jaunmarupe_Bogwoodland_CHM/`. The CHM records vegetation height above the ground surface and is the complementary layer for woodland structure and habitat condition analysis.
