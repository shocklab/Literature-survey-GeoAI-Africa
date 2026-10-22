# Numbers derived from the extraction spreadsheet

Source: `figures/source/Reviewed_articles_only.xlsx`, 138 studies.
Regenerate with `python3 figures/build_figures.py`.

| Quantity | Value from data | Against the paper |
|---|---|---|
| Publications per year | 2016=4, 2017=4, 2018=2, 2019=5, 2020=12, 2021=13, 2022=13, 2023=14, 2024=24, 2025=31, 2026=16 (sum 138) | PNG had 2024=25, 2025=32, 2026=15 |
| Application domains | Agriculture 43 (31.2%); Urban & Infrastructure 38 (27.5%); Climate & Environment 32 (23.2%); Disaster Response 16 (11.6%); Public Health 9 (6.5%) | matches the paper |
| Random Forest | algorithm 79; family 83 (adds Canonical Correlation Forest, Extra Trees) |  |
| Method denominators | classical n=104, deep n=62 | paper implies 102 and 63 |
| Classical families | Random forest 83; SVM 35; Gradient boosting 20; Decision tree 12; Linear & probabilistic 11; k-NN 8; Clustering 5 |  |
| Deep families | Feedforward network 23; CNN - classification 22; CNN - segmentation 20; Self-supervised and representation learning 5; CNN - detection 4; Transformer 4; Spatio-temporal 4; Recurrent 2; Semi-supervised segmentation 1 |  |
| Learning paradigm, exclusive assignment | Supervised 126 (91.3%); Unsupervised 3 (2.2%); Self-supervised 5 (3.6%); Semi-supervised 1 (0.7%); Foundation / pretrained 2 (1.4%) | paper says supervised 91.3%% - MATCHES exactly |
| Model category by year | 2016: 3/2/0; 2017: 4/0/0; 2018: 2/0/0; 2019: 4/3/0; 2020: 10/4/0; 2021: 13/2/0; 2022: 9/6/0; 2023: 11/9/0; 2024: 19/10/1; 2025: 16/19/0; 2026: 13/7/1 | order: classical/deep/foundation |
| Journals | 23 venues with >=2 studies covering 88 of 138; 11 with >=3 covering 64 | fig-journals previously said 12 venues covering 65 |
| Resolution classes | Coarse (>100 m) 27; Moderate (10-100 m) 52; High (1-10 m) 71; Very high (<1 m) 26 (of 130 with EO data) |  |
| Acquisition platform | Satellite 124; UAV 10; Manned aircraft 3 | base for the paper's EO percentages is the 124 satellite studies |
| Spatio-temporal spans | 60 of 138 studies record a date range; Single year 6; Short (1--5 yr) 13; Medium (6--15 yr) 19; Long ($>$15 yr) 22 |  |
| Spatio-temporal Sankey | 58 of 60 span-reporting studies drawn; applications Urban & settlement 16.0; Crop & yield 14.0; LULC & deforestation 11.0; Drought & degradation 7.0; Burned area 5.0; Flood & landslide 4.0; Public health 1.0 | data Landsat / HLS 24.0; Coarse (>100 m) 6.4; Sentinel-2 8.9; PlanetScope / RapidEye 3.3; SAR 4.9; Weather series 10.4 |  |
| GEE | 61/69 = 88.4% | paper 86.4% - matches |
| NDVI | 65/79 = 82.3% | paper 82.3% - matches |
| Top-3 countries | South Africa 24 (19.5%); Kenya 18 (14.6%); Nigeria 15 (12.2%); combined 57/123 = 46.3% | paper says 43.9% (n=54/123) - the COMBINED figure is wrong |
| Sentinel-2 | 57/124 satellite studies = 46.0% | paper 46.0% - MATCHES; the base is the 124 satellite studies, not 130 |
| Landsat, any | 48/124 = 38.7% | paper 37.9% (n=47); data gives 48, so one study differs |
| Satellite / airborne split | satellite only 117 (84.8%); satellite+airborne 7 (5.1%); airborne only 6 (4.3%) | paper 85.5% (118/138) / 5.1% / 4.3% - last two MATCH, first is 117 not 118 |
| Geographic extent | Single country 95; Multiple countries 22; Continental 12; Congo Basin 3; Sub-Saharan Africa 3; Horn of Africa 1; West Africa 1; Nile Basin 1 | paper L238: 95 / 22 / 9 sub-regional / 12 |
| Weather sources | CHIRPS 15; Weather station 5; ERA5 / ERA5-Land 4; WorldClim 3; TAMSAT 2; CRU TS 2; TerraClimate 2; aWhere 1; 37 studies | paper: CHIRPS 40% of weather-data studies |
| DEM sources | SRTM 27; ASTER GDEM 5; AW3D30 4; NASADEM 3; UAV / Drone SfM 2; MERIT 2; 40 studies | paper: SRTM 67.5% (27/40) |
| Platforms | Google Earth Engine 61; Local / national HPC 7; Google Colab 4; AWS 3; Google Cloud Platform 2; Hugging Face 1; ESA CloudToolbox 1; Sentinel Hub 1; Planet Explorer Portal 1; Microsoft Azure 1; SEPAL (FAO) 1; Digital Earth Africa 1; Microsoft Planetary Computer 1; NASA Earth Exchange 1; 69 studies name one; single 57, several 12 | Ian: 69 / 61 GEE / 57 / 12 |
| Open science | repository 25; data link 33; interactive 5 | PNG caption: 25 repositories |
| Author institutions | 518 institution rows over 138 studies, 56 countries; top: US 52; ZA 24; DE 24; GB 22; IT 13; CN 12; NL 12; KE 11; FR 10; BE 10; NG 9; CA 7; GH 6 | OpenAlex via fetch_affiliations.py; coded by hand: studies 99, 115, 121, 127 |
| Collaboration | African-only 24; North-South 50; Non-African-only 64; any African institution 74 (53.6%); single institution 25; multi-institution single-country 29; multi-country 84 | fig-collaboration (b) |
| Cross-sector partners | 64 cross-sector studies (46.4%); academic only 67 (48.6%); no academic institution 7; partner institutions: Research facility 70; Government / intergovernmental 34; Non-profit / NGO 32; Company 10 | earlier hand count: facility 86, nonprofit 33, government 32, company 10 |
| PRISMA | identified 928; removed before screening 655 (duplicates 108, limits 65, ACM keyword filter 482); screened 273; excluded 96; sought 177; not retrieved 2; assessed 175; excluded 74; databases 101 + citation searching 37 = 138 | 0 studies with no Source |
