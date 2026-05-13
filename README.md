# Jaunmārupe Bogwoodland Project

## Overview

This repository contains the spatial data, processing scripts, and supporting
documentation for the **Jaunmārupe Bogwoodland Biodiversity Credit Project**,
developed by **aeco GmbH** in partnership with **Rīgas meži (Riga Forests Ltd.)**.

The project proposes the restoration of a degraded raised bog and bog woodland
ecosystem in Mārupes novads, Latvia, and is being developed under the
**Wallacea Trust / Biodiversity Futures Initiative (BFI) Biodiversity Credit
Methodology V3** as a biodiversity uplift project.

---

## Project Site Summary

| Field | Details |
|---|---|
| **Site name** | Jaunmārupe Bogwoodland |
| **Location** | Mārupes novads, Latvia |
| **Centre coordinates** | 56.835374°N, 23.912221°E |
| **Project area** | 1,992 ha |
| **Ecosystem type** | IUCN TF1.6 Boreal, temperate and montane peat bogs |
| **Project period** | 2026–2046 (20 years) |
| **Standard** | Wallacea Trust Biodiversity Credit Methodology V3 |
| **Project developer** | aeco GmbH (Berlin, Germany) |
| **Land manager** | Rīgas meži (Riga Forests Ltd., Riga, Latvia) |
| **Landowner** | Riga Municipality |
| **Reference site** | Natura 2000 NR "Cenas Tīrelis" (LV0519800, 2,133 ha) |
| **BFI application** | Stage 1 Application submitted May 2026 |

---

## Site Description

The Jaunmārupe Bogwoodland is a degraded raised bog located within the wider
Cenas Tīrelis mire complex, directly adjacent to the Natura 2000 Nature Reserve
"Cenas Tīrelis" (LV0519800) to the northwest. 

The proposed restoration programme involves systematic ditch blocking and
infilling to raise the water table, combined with
forest restructuring and invasive species control, targeting recovery of EU
Habitats Directive priority habitat types 7110* (Active raised bogs) and
91D0* (Bog woodland) over the 20-year project period.

---

## Metric Basket

| Metric | Taxa | Type | Survey method |
|---|---|---|---|
| M1 | Water table depth | Structural (S) | 15 loggers (project site) + 5 loggers (reference site) |
| M2 | Vascular plants | Compositional (C) | Transects + relevé plots — field botanist |
| M3 | Mosses / Bryophyta | Compositional (C) | Co-located with M2 |
| M4 | Dragonflies / Odonata | Compositional (C) | Field transects — specialist (Mārtiņš Kalns) |
| M5 | Butterflies / Lepidoptera | Compositional (C) | eBMS transects — trained naturalist |
| M6 Additional | Canopy cover | Management verification | Remote sensing + field densiometer |

---

## Repository Structure

```
Jaunmārupe Bogwoodland Project/
│
├── README.md                               # This file
│
├── maps/
│   ├── project_boundary/
│   │   ├── jaunmarupe_boundary.gpkg
│   │   └── jaunmarupe_boundary_metadata.txt
│   ├── habitat_map/
│   │   ├── eunis_habitat_map_jaunmarupe.gpkg
│   │   ├── eunis_habitat_map_jaunmarupe_final.png
│   │   └── eunis_habitat_map_metadata.txt
│   ├── reference_site/
│   │   ├── cenas_tirelis_NR_boundary.gpkg
│   │   └── cenas_tirelis_NR_metadata.txt
│   ├── landscape_context/
│   │   ├── jaunmarupe_surrounding_areas.gpkg
│   │   └── jaunmarupe_surrounding_areas.png
│   └── leakage_zone/
│       ├── leakage_zone_500m_buffer.gpkg
│       └── leakage_zone_metadata.txt
│
├── scripts/
│   ├── habitat_map/
│   │   ├── eunis_habitat_classification.py     # EUNIS probability model processing
│   │   └── canopy_height_verification.py       # Meta/GLAD CHM forest fill
│   ├── maps/
│   │   ├── landscape_context_map.py            # Produces Q8 figure
│   │   └── habitat_map_figure.py               # Produces Q9 figure
│   └── remote_sensing/
│       ├── ndmi_surface_water.py               # Sentinel-2 NDMI bare peat analysis
│       └── water_table_proxy.py                # ET proxy + SAR water level dynamics
│
├── monitoring/
│   ├── water_table/
│   │   └── logger_placement_design.gpkg        # To be added once finalised
│   ├── vegetation/
│   │   └── transect_plot_design.gpkg           # To be added once finalised
│   ├── odonata/
│   │   └── transect_design.gpkg                # To be added once finalised
│   └── butterflies/
│       └── transect_design.gpkg                # To be added once finalised
│
└── data/
    ├── raw/
    │   ├── drainage_network/
    │   │   └── purva_gravji.gpkg               # Main ditch network from Rīgas meži
    │   ├── elevation/
    │   │   └── dtm_1m_metadata.txt             # 1m DTM (data too large for repo)
    │   └── satellite/
    │       └── ndmi_summer2023_metadata.txt    # Sentinel-2 NDMI metadata
    └── processed/
        └── habitat_classification/
            └── eunis_classified_raster_metadata.txt


```

---

## Data Notes

Large raster datasets (1 m DTM, Sentinel-2 imagery, Global Canopy Height Model)
are not stored directly in this repository due to file size constraints. Metadata
files in `data/raw/` provide full source references, acquisition dates, and
coordinate reference systems for all datasets used.

All vector spatial data is provided in GeoPackage (.gpkg) format, coordinate
reference system EPSG:3035 (ETRS89 / LAEA Europe) unless otherwise stated.

---

## Dependencies

Python scripts require the following packages:

```bash
pip install geopandas rasterio numpy matplotlib earthengine-api
```

Google Earth Engine authentication is required for remote sensing scripts.
See [GEE documentation](https://developers.google.com/earth-engine/guides/auth)
for setup instructions.

---

## Contact

**Dr. Talita Ferreira Amado**
Biodiversity Project Developer
aeco GmbH
t.amado@aeco.earth
[www.aeco.earth](https://www.aeco.earth)

---

## License

Spatial data and scripts in this repository are made available under the
[Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
Please cite this repository and the associated BFI Stage 1 Application when
using these materials.

---

## Citation

aeco GmbH (2026). *Jaunmārupe Bogwoodland Project — Spatial Data and Scripts.*
GitHub repository. https://github.com/aeco-earth/jaunmarupe-bogwoodland-project


