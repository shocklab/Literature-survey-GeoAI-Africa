# Literature-survey-GeoAI-Africa

Study records and figure code for the review "GeoAI for Africa: A Survey of Data Gaps, Methods, and the
Path Toward Inclusive Geospatial Intelligence" (Ocholla, Alaagib, Hacheme, Gbodjo, Tadesse and Shock).
Each release is archived on Zenodo: https://doi.org/10.5281/zenodo.22745736 resolves to the latest version.

## Contents

| Path | What it is |
|---|---|
| `figures/source/Reviewed_articles_only.xlsx` | The included studies and their coded attributes. `Studies` has one row per study; `Selected_articles` holds the full extraction; the `*_long` sheets list methods, EO data, indices, countries, weather and DEM sources, tasks, platforms and journals one entry per row; `PRISMA` holds the search and screening counts; `Abbreviations` expands the short forms. |
| `figures/source/lookups.json` | Mappings from the names used in the workbook to the categories in the figures (methods, sensors, platforms, weather products, repository types, spatio-temporal categories, ISO3 country codes). |
| `figures/source/Africa_Countries.geojson` | Country boundaries for the map. |
| `figures/build_figures.py` | Generates the figures, and the counts quoted in the text, from the three source files. |
| `figures/check_supp_refs.py` | Checks that each "Table S*n*" in the manuscript refers to a table the supplementary defines. |
| `figures/style.tex` | Colours and styles shared by the figures. |
| `figures/fig-*.tex` | The figures, as TikZ and pgfplots. `fig-prisma.tex` is drawn by hand with its counts taken from `numbers.tex`; the rest are generated. |

## Generating the figures and counts

```
pip install -r figures/requirements.txt
python3 figures/build_figures.py
```

The script finds its inputs relative to its own location, so it can be run from any directory. It writes
`fig-yearly.tex`, `fig-domain.tex`, `fig-methods.tex`, `fig-models-year.tex`, `fig-journals.tex`,
`fig-spatiotemporal.tex`, `fig-resolution.tex`, `fig-infrastructure.tex` and `fig-choropleth.tex` to `figures/`, and two files to
`figures/generated/`:

- `numbers.tex`, the counts and percentages quoted in the text, one `\newcommand` each, for example
  `\nStudies` for the number of included studies;
- `NUMBERS.md`, every derived number with its definition.

Re-run it after any change to the workbook, then copy the figure files and `numbers.tex` into the
manuscript's `figures/` folder.

## Using the output in LaTeX

The manuscript loads the styles and counts in its preamble, after `pgfplots` and the TikZ libraries
`arrows.meta`, `positioning`, `calc`, `fit` and `backgrounds`:

```latex
\input{figures/style.tex}
\input{figures/numbers.tex}
```

Each figure is then included with `\input{figures/fig-yearly.tex}` and so on, and counts are written as
macros: `\nStudies{} studies`, `\pctSentinelTwo\%`.

## Checking supplementary table references

From the folder that holds `manuscript_review.tex` and `supplementary_S1.tex`:

```
python3 figures/check_supp_refs.py
```

or give that folder as an argument from anywhere else. It lists each supplementary table with its number
and whether the main text cites it, and exits with status 1 if the main text cites a table number the
supplementary does not define or the supplementary has a table the script does not know.

## Licence

Apache License 2.0; see `LICENSE`.
