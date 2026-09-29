#!/usr/bin/env python3
"""Check that every "Table SN" in the manuscript points at the table the
supplementary actually numbers SN.

The supplementary sets \renewcommand{\thetable}{S\arabic{table}}, so its tables
are numbered S1, S2, ... in the order they appear in the file. The manuscript
refers to them as plain text, which is what Elsevier wants for supplementary
material but gives LaTeX no way to catch drift. Run this after moving,
adding or deleting a supplementary table.

    python3 figures/check_supp_refs.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAIN = next((p for p in (HERE.parent.parent / "manuscript_review.tex",
                         HERE.parent.parent / "main.tex") if p.exists()), None)
if MAIN is None:
    sys.exit("main text not found (looked for manuscript_review.tex, main.tex)")
SUPP = HERE.parent.parent / "supplementary_S1.tex"   # claude/supplementary_S1.tex

# What each S-number is expected to be about, keyed by the supplementary's own
# label. Edit this when a table is added or its subject changes.
EXPECTED = {
    "tab:eo_data": "Earth observation data sources",
    "tab:eo_indices": "EO-derived features and indices",
    "tab:dem_derivatives": "DEM derivatives / terrain",
    "tab:climate_datasets_compact": "climate and weather products",
    "tab:pop_socio": "population and socioeconomic data",
    "tab:agri_data": "agricultural datasets",
    "tab:disaster_data": "disaster datasets",
    "tab:landcover_data": "land cover datasets",
}

_supp = SUPP.read_text()
_supp = re.sub(r"\\begin\{comment\}.*?\\end\{comment\}", "", _supp, flags=re.S)   # commented-out tables do not get a number
_supp = re.sub(r"(?<!\\)%.*", "", _supp)
labels = re.findall(r"\\label\{(tab:[^}]+)\}", _supp)
numbering = {f"S{i}": lab for i, lab in enumerate(labels, 1)}

main = MAIN.read_text()
main = re.sub(r"%.*", "", main)                       # ignore commented-out text
main = re.sub(r"\\query\{[^{}]*(\{[^{}]*\}[^{}]*)*\}", "", main)   # ignore queries
cited_raw = sorted(set(re.findall(r"Tables?[~ ]*(S\d+)(?:\s*(?:and|,)\s*(S\d+))?", main)), key=lambda t: int(t[0][1:]))
cited = sorted({n for pair in cited_raw for n in pair if n}, key=lambda x: int(x[1:]))

problems = []
print(f"supplementary defines {len(labels)} tables\n")
for num, lab in numbering.items():
    mark = "cited" if num in cited else "NOT CITED"
    print(f"  {num:<4} {lab:<32} {EXPECTED.get(lab,'?'):<34} {mark}")
    if lab not in EXPECTED:
        problems.append(f"{num} ({lab}) is not in EXPECTED; update this script.")

for num in cited:
    if num not in numbering:
        problems.append(f"main text cites Table {num}, but the supplementary "
                        f"only numbers up to S{len(labels)}.")

uncited = [n for n in numbering if n not in cited]
if uncited:
    print(f"\nnever referenced from the main text: {', '.join(sorted(uncited, key=lambda x: int(x[1:])))}")

if problems:
    print("\nPROBLEMS")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("\nnumbering is consistent.")
