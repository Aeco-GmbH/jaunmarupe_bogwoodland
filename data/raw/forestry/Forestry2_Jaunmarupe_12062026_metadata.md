# Forestry2_Jaunmarupe_12062026 — Forest Stand Inventory

## Summary

| Property | Value |
|---|---|
| File | `Forestry2_Jaunmarupe_12062026` |
| Format | GeoPackage (no `.gpkg` extension) |
| Layer | `nogabali__nogabali_db` |
| Geometry type | MultiPolygon |
| Features | 197 |
| Total area | 667.6 ha |
| CRS | EPSG:25884 (ETRS89 / TM Baltic93) |
| Inventory dates | 2015 – May 2026 |
| Downloaded | 12 June 2026 |

## Description

Detailed forest stand inventory (*nogabali*) for the Jaunmārupe project area,
sourced from the Rīgas meži forest management database. Each polygon represents
a forest stand compartment with full dendrometric data: species composition, age,
height, diameter, basal area, growing stock, silvicultural prescriptions, and
protected species flags.

This is the primary data source for forest structure characterisation, baseline
carbon stock estimation, and habitat condition assessment in the biodiversity
credit application.

## Stand composition

### Dominant tree species (`mt`)

| Code | Species | Stands |
|---|---|---|
| As | *Populus tremula* (Aspen) | 58 |
| Ks | *Pinus sylvestris* (Scots pine) | 48 |
| Km | *Betula pubescens* (Downy birch) | 33 |
| Dm | *Alnus glutinosa* (Black alder) | 15 |
| Ln | *Tilia cordata* (Small-leaved lime) | 13 |
| Ap | *Picea abies* (Norway spruce) | 8 |
| Mr | *Alnus incana* (Grey alder) | 7 |
| Am | *Acer* spp. (Maple) | 4 |
| Dms | *Alnus glutinosa* subsp. | 4 |
| Other | Various | 5 |

### Age structure (`vec_grupa`)

| Age group | Latvian | Stands |
|---|---|---|
| Middle-aged | Vidēja vecuma audzes | 84 |
| Mature | Pieaugušās audzes | 42 |
| Young | Jaunaudzes | 26 |
| Maturing | Briestaudzes | 25 |

## Attributes

| Column | Latvian term | Description |
|---|---|---|
| `meznieciba` | Mežniecība | Forest district |
| `iecirknis` | Iecirknis | Forest section |
| `apgaita` | Apgaita | Management unit |
| `kadnum` | Kadastra numurs | Cadastral parcel number |
| `kvartals` | Kvartāls | Forest compartment number |
| `nogabals` | Nogabals | Stand number within compartment |
| `apaksnog` | Apakšnogabals | Sub-stand number |
| `atslega` | Atslēga | Unique stand key |
| `nog_plat` | Nogabala platība | Stand area (ha) |
| `meza_plat` | Meža platība | Forested area (ha) |
| `celu_plat` | Ceļu platība | Road area within stand (ha) |
| `gravju_plat` | Grāvju platība | Ditch area within stand (ha) |
| `year` | Gads | Data year |
| `zkat` | Zemes kategorija | Land category (Mežaudze = forest stand) |
| `mt` | Mežaudzes tips | Dominant tree species code |
| `biez` | Biezība | Stand density (0–10 scale) |
| `skersl` | Šķērslaukums | Mean basal area (m²/ha) |
| `formula` | Formula | Stand composition formula (e.g. 10B60 = 100% birch age 60) |
| `izcelsme` | Izcelsme | Stand origin (Dabiska = natural, Mākslīga = planted) |
| `bon` | Bonitete | Site quality class (I = best) |
| `kraja` | Krāja | Growing stock volume (m³/ha) |
| `gtf_nature` | — | Last inventory year |
| `vec_grupa` | Vecuma grupa | Age group |
| `s_vald` | Sugas vald. | Dominant species code |
| `a_vald` | Age (dominant species) | Age of dominant species (years) |
| `h_vald` | Height (dominant) | Mean height of dominant species (m) |
| `d_vald` | Diameter (dominant) | Mean diameter of dominant species (cm) |
| `g_vald` | Basal area (dominant) | Basal area of dominant species (m²/ha) |
| `koc_vald` | Koku skaits | Stem count of dominant species (per ha) |
| `jakopj` | Jākopj | Tending prescription flag |
| `jaatjauno` | Jāatjauno | Regeneration prescription flag |
| `p_darbv` | Plānotā darbības veids | Planned operation type |
| `p_darbg` | Plānotā darbības gads | Planned operation year |
| `p_cirg` | Plānotā cirtes gads | Planned felling year |
| `p_cirp` | Plānotā cirtes pamatojums | Planned felling justification |
| `va_kods1–5` | Vides aizsardzības kodi | Environmental protection codes (up to 5) |
| `aizs_1–5` | Aizsardzības statuss | Protection status flags |
| `va_unik_1–5` | Vides aizsardzības unikālie kodi | Unique environmental protection IDs |
| `ipatn1–5` | Īpatnības | Special features / remarks |
| `saimn_d_ierob` | Saimnieciskās darbības ierobežojumi | Management activity restrictions |
| `pagasts` | Pagasts | Parish (administrative unit) |
| `plant_audze` | Plantāciju audze | Plantation flag |
| `invent_dat` | Inventarizācijas datums | Last inventory date |
| `krasa` | Krāsa | Display colour code (QGIS symbology) |
| `iadt` | IADT | Protected area code (if within IADT) |
| `ml` | Medību liegums | Hunting restriction flag |
| `putnu_ml` | Putnu medību liegums | Bird hunting restriction flag |
| `rm_aprob` | RM aprobežojumi | Rīgas meži management restrictions |

## Relevance to the Jaunmārupe project

This is the core forest stand dataset for the project. Key uses:

- **Baseline habitat condition**: species composition, age, and density data
  characterise the current state of bog woodland (EUNIS Q54 / Natura 2000 91D0)
  and degraded bog habitats across the project area.
- **Carbon baseline**: growing stock volumes (`kraja`) combined with allometric
  equations provide above-ground biomass and carbon stock estimates per stand.
- **Restoration prioritisation**: age groups, thinning prescriptions (`jakopj`),
  and drainage area (`gravju_plat`) identify stands most in need of intervention.
- **Protected species context**: environmental protection codes (`va_kods1–5`)
  flag stands with legally protected species or habitats.

## Data source

Rīgas meži (Riga Municipality Forest Service)  
Exported from the Rīgas meži forest management information system on 12 June 2026.

## Coordinate reference system

EPSG:25884 — ETRS89 / TM Baltic93  
Baltic states projected CRS. Units: metres.
