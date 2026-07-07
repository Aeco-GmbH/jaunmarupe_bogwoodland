# Habitat_SemiAutomaticClassification_20262105.tif

> **Note for repository reviewers:** This raster file is excluded from the repository
> due to its size (~73 MB). Download it from Google Drive:
> [Habitat_SemiAutomaticClassification_20262105.tif](https://drive.google.com/file/d/12vJvFW9CVD8ZvsfaJTga1BQe-h_SoPx_/view?usp=share_link)
>
> Place the downloaded file in this folder (`05_analyses/`) before running any
> analysis scripts that reference it.

## Summary

| Property | Value |
|---|---|
| File | `Habitat_SemiAutomaticClassification_20262105.tif` |
| Format | GeoTIFF |
| Date | 21 May 2026 |
| Classification type | Semi-automatic supervised classification |
| CRS | EPSG:3059 (LKS92 / Latvia TM) |
| Resolution | 2 m/pixel |
| Dimensions | 4,406 × 4,163 pixels |
| Bands | 1 |
| Data type | Float32 |
| NoData value | −3.4 × 10³⁸ (float32 minimum) |
| Classified area | 1,992.3 ha |

## Description

A semi-automatic supervised habitat classification of the Jaunmārupe project area,
produced using the Semi-Automatic Classification Plugin (SCP) for QGIS. The
classification maps seven habitat classes across the ~1,993 ha project boundary,
providing a spatial baseline for the biodiversity credit application.

The full methodology — including input data sources, preprocessing steps,
classification algorithm, and accuracy assessment — is described in **Annex 1 of
the Stage 1 Application** (BFI Application, Jaunmārupe Bogwoodland Biodiversity
Credit Project).

## Habitat classes

| Pixel value | Habitat class | Area (ha) | % of total |
|---|---|---|---|
| 101 | Bog woodland | 269.0 | 13.5% |
| 102 | Forested peat extraction site | 154.4 | 7.7% |
| 201 | Raised bogs with shrubs | 1,045.0 | 52.5% |
| 202 | Open peat extraction site — dry | 204.9 | 10.3% |
| 203 | Open peat extraction site — wet | 238.2 | 12.0% |
| 301 | Water | 28.0 | 1.4% |
| 401 | Dunes | 52.6 | 2.6% |

> **Note:** Pixel values follow the SCP (Semi-Automatic Classification Plugin) macroclass
> and class ID convention. Unclassified pixels are stored as NoData. Verify the exact
> pixel-to-class mapping against the SCP project file if needed.

## Companion files

| File | Description |
|---|---|
| `Habitat_SemiAutomaticClassification_20262105.tif.aux.xml` | Raster statistics (min, max, mean, std dev) — included in the repository |
| `TrainingDataHabitat.gpkg` | Training polygons (80 features, 13 habitat labels) used for the supervised classification — included in the repository |

## Relevance to the Jaunmārupe project

This classification layer is used to:

- **Map habitat extent**: quantify the area of each habitat type within the project
  boundary as part of the biodiversity baseline.
- **Identify restoration targets**: locate degraded habitats (active peat extraction,
  forested peat extraction sites) that are candidates for rewetting and restoration.
- **Support credit calculations**: provide the spatial foundation for habitat condition
  scoring and biodiversity credit quantification under the Wallacea Trust standard.

## Coordinate reference system

EPSG:3059 — LKS92 / Latvia TM  
Latvian national projected CRS. Units: metres.

## Data source

Produced by aeco GmbH, May 2026, as part of the EU LIFE BiodivCrEW project
(Jaunmārupe Bogwoodland Biodiversity Credit Project, Stage 1 Application).
