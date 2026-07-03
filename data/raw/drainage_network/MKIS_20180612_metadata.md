# MKIS_20180612.gdb — Latvian Melioration Cadastral Information System

## Summary

| Property | Value |
|---|---|
| File | `MKIS_20180612.gdb` |
| Format | ESRI File Geodatabase |
| Full name | Meliorācijas Kadastra Informācijas Sistēma (MKIS) |
| Translation | Melioration Cadastral Information System |
| Coverage | National (all of Latvia) |
| Export date | 12 June 2018 |
| Layers | 15 |
| CRS | EPSG:3059 (LKS92 / Latvia TM) |
| Source | Latvijas Lauku atbalsta dienests (LAD) — Rural Support Service of Latvia |

## Description

The MKIS is the national cadastral registry of Latvia's agricultural drainage and
melioration infrastructure. It documents the complete network of open ditches,
subsurface drainage pipes, drain collectors, rivers, polders, pumping stations,
and hydraulic structures built primarily during the Soviet period (1950s–1990s) to
drain wetlands and peatlands for agricultural use.

The network is extremely dense — Latvia has one of the most extensive artificial
drainage systems in Europe, with over 715,000 km of underground drainpipes alone.
Within the Jaunmārupe project area, this infrastructure is the primary driver of
peatland degradation through continuous water table lowering.

## Layers

| Layer | Geometry | Features | Total length / area | Description |
|---|---|---|---|---|
| `Drainpipes` | MultiLineString | 6,908,446 | 715,893 km | Underground subsurface drainage pipes |
| `DrainCollectors` | MultiLineString | 1,480,406 | 151,534 km | Collector drains aggregating drainpipe outflow |
| `Ditches` | MultiLineString | 167,959 | 72,026 km | Open drainage ditches |
| `StateRiversLine` | MultiLineString | 2,053 | 24,421 km | State-controlled rivers (line representation) |
| `BigDrainCollectors` | MultiLineString | 6,254 | 2,058 km | Major collector drains |
| `Dam` | MultiLineString | 125 | 489 km | Dams and embankments |
| `StateRiversPolygon` | MultiPolygon | 1,783 | 43,609 ha | State-controlled rivers (polygon representation) |
| `PolderTerritory` | MultiPolygon | 48 | 36,021 ha | Polder areas with pumped drainage |
| `Catchment` | MultiPolygon | 4,702 | 6,579,157 ha | Drainage catchment areas |
| `NetworkStructures` | Point | 170,312 | — | Drainage network structures (sluices, outlets) |
| `TransportStructures` | Point | 57,038 | — | Culverts and bridges over drainage infrastructure |
| `HydroPost` | Point | 56 | — | Hydrological monitoring stations |
| `PolderPumpingStation` | Point | 60 | — | Polder pumping stations |
| `HydrotechnicsStructures` | Point | 89 | — | Hydraulic engineering structures |
| `StateControlledRivers` | MultiLineString | 1,591 | 13,773 km | State-managed rivers with catchment metadata |

## Key attribute fields

### Linear drainage layers (Ditches, DrainCollectors, Drainpipes)

| Column | Description |
|---|---|
| `Kods` | Feature type code |
| `Diameter` | Pipe/collector diameter (cm, where applicable) |
| `ObjCode` | Object code |
| `SysCode` | System code |
| `Numb` | Feature number within system |
| `Code` | Drainage system code |
| `Shape_Length` | Feature length (m) |

### StateControlledRivers

| Column | Description |
|---|---|
| `Code` | River identifier code |
| `Name` | River name |
| `GrandCatchment` | Grand catchment ID |
| `SummLength` | Total river length (m) |
| `CatchmentArea` | Catchment area (km²) |
| `LastBuildYear` | Last construction/regulation year |

### PolderTerritory

| Column | Description |
|---|---|
| `Name` | Polder name |
| `HeightMesurement` | Reference elevation for pumping (m a.s.l.) |

## Layers used in Jaunmārupe analyses

Three layers are clipped and used directly in project scripts:

| Layer | Used in | Purpose |
|---|---|---|
| `Ditches` | `hydrology_map.py` | Mapped as blue lines — open drainage ditches |
| `DrainCollectors` | `hydrology_map.py`, `dtm_rewetting_map.py` | Mapped as orange lines; crossing points with project boundary identified as candidate drain-blocking locations |
| `Drainpipes` | `hydrology_map.py` | Mapped as grey lines — subsurface tile drainage |

## Relevance to the Jaunmārupe project

The MKIS dataset documents the drainage infrastructure that has caused and
continues to drive peatland degradation within the Jaunmārupe project area.
Key uses in the biodiversity credit application:

- **Baseline threat documentation**: density and extent of drainage infrastructure
  within the project boundary demonstrates the severity of hydrological degradation.
- **Restoration planning**: drain collector crossing points at the project boundary
  are candidate locations for drain blocking, the primary rewetting intervention.
- **Additionality**: the active, maintained drainage network demonstrates that
  without intervention, degradation will continue.

## Data source

Latvijas Lauku atbalsta dienests (LAD) — Rural Support Service of Latvia  
MKIS open data portal: https://www.lad.gov.lv/lv/melioracijas-kada strs  
Exported 12 June 2018. National coverage snapshot.  
Licence: Open government data (Latvian Open Data Licence).

## Coordinate reference system

EPSG:3059 — LKS92 / Latvia TM  
Latvian national projected CRS. Units: metres. Datum: LKS92 (Latvia Coordinate System 1992).
