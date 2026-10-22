#!/usr/bin/env python3
"""
Look up the author institutions of every included study in OpenAlex and write
them to the institutions_long sheet of the workbook, one row per study and
distinct institution:

    study_id, institution, openalex_id, country (ISO2), type, academic_parent, source

academic_parent is the university the institution belongs to in OpenAlex's
lineage, if any: a department, institute or laboratory of a university counts
as academic in the collaboration figure, whatever OpenAlex types it. Then the
six affiliation columns of the Studies sheet are refreshed from that sheet
(n_institutions, inst_countries, collab_breadth, has_african_inst,
african_leadership, cross_sector), so the workbook stays self-consistent.

    python3 figures/fetch_affiliations.py [--dry-run]

Reads study_id, Title and "DOI / link" from the Studies sheet. A study without
a DOI is looked up by title. Rows whose source starts with "manual" are kept
across runs, so institutions OpenAlex does not know can be entered by hand;
they are dropped for a study once OpenAlex returns institutions for it, unless
the study is listed in pinned_studies in lookups.json, in which case OpenAlex
is not consulted and the manual rows stand. Every "openalex" row is replaced.
Institutions are de-duplicated by name within a study (OpenAlex sometimes lists
one institute under two ids), and an institution with no country code takes
the country of its parent in OpenAlex's lineage. Needs network access;
build_figures.py does not, so run this only when the corpus changes, then
re-run build_figures.py.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
WB = HERE / "source" / "Reviewed_articles_only.xlsx"
LK = json.loads((HERE / "source" / "lookups.json").read_text(encoding="utf-8"))
SHEET = "institutions_long"
COLS = ["study_id", "institution", "openalex_id", "country", "type", "academic_parent", "source"]
MAILTO = "ian.ocholla@uct.ac.za"
DRY = "--dry-run" in sys.argv
AFRICA = set(LK["iso2_africa"])


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "geoai-africa-review/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def by_doi(doi):
    return get(f"https://api.openalex.org/works/doi:{doi}?mailto={MAILTO}")


def by_title(title):
    q = urllib.parse.quote(re.sub(r"[^\w\s]", " ", title)[:200])
    res = get(f"https://api.openalex.org/works?filter=title.search:{q}&per-page=3&mailto={MAILTO}")["results"]
    return res[0] if res else None


_inst_cache = {}


def inst_record(iid):
    """The OpenAlex institution record, cached; {} if it cannot be fetched."""
    if iid not in _inst_cache:
        try:
            _inst_cache[iid] = get(f"https://api.openalex.org/institutions/{iid.rsplit('/', 1)[-1]}?mailto={MAILTO}")
        except Exception:
            _inst_cache[iid] = {}
        time.sleep(0.12)
    return _inst_cache[iid]


def parents(inst):
    return [x for x in inst.get("lineage", []) if x != inst.get("id")]


def country_of(inst):
    """The institution's country code, or its nearest lineage parent's."""
    if inst.get("country_code"):
        return inst["country_code"]
    for iid in [inst.get("id")] + parents(inst):
        if iid and inst_record(iid).get("country_code"):
            return inst_record(iid)["country_code"]
    return ""


def academic_parent_of(inst):
    """The nearest university in the institution's lineage, or ""."""
    for iid in parents(inst):
        if inst_record(iid).get("type") == "education":
            return inst_record(iid).get("display_name") or ""
    return ""


def institutions(work):
    seen = {}
    for a in work.get("authorships", []):
        for i in a.get("institutions", []):
            name = (i.get("display_name") or "").strip()
            key = re.sub(r"[^a-z0-9]", "", name.lower())
            if name and key not in seen:
                cc = LK["institution_country_overrides"].get(name) or country_of(i)
                seen[key] = (name, (i.get("id") or "").rsplit("/", 1)[-1], cc, i.get("type") or "",
                             academic_parent_of(i))
    return list(seen.values())


def category(name, tp, academic_parent):
    """The partner category of an institution: a named override first, then
    academic for any sub-unit of a university, then the OpenAlex type."""
    if name in LK["institution_type_overrides"]:
        return LK["institution_type_overrides"][name]
    if academic_parent:
        return "Academic"
    return LK["institution_types"].get(tp)


wb = openpyxl.load_workbook(WB)
st = wb["Studies"]
hdr = [c.value for c in st[1]]
col = {h: i for i, h in enumerate(hdr)}
studies = [(str(r[col["study_id"]]), r[col["DOI / link"]], r[col["Title"]])
           for r in st.iter_rows(min_row=2, values_only=True) if r[col["study_id"]] is not None]

manual = []
if SHEET in wb.sheetnames:
    oh = [c.value for c in wb[SHEET][1]]
    for r in wb[SHEET].iter_rows(min_row=2, values_only=True):
        d = dict(zip(oh, r))
        if str(d.get("source") or "").startswith("manual"):
            manual.append([d.get(c) for c in COLS])

pinned = {str(k) for k in LK.get("pinned_studies", {})}
rows, missing, errors = [], [], []
for sid, link, title in studies:
    if sid in pinned:
        print("  %s: pinned in lookups.json, OpenAlex not consulted" % sid)
        continue
    m = re.search(r"10\.\d{4,9}/\S+", str(link or ""))
    try:
        if m:
            work = by_doi(m.group(0).rstrip(".)"))
        else:
            work = by_title(str(title or ""))
            if work:
                print("  %s: no DOI; title search matched '%s'" % (sid, work.get("display_name", "")[:70]))
    except Exception as e:
        errors.append((sid, str(e)[:60]))
        time.sleep(0.2)
        continue
    insts = institutions(work) if work else []
    if not insts:
        missing.append(sid)
    for name, oid, cc, tp, ap in insts:
        if not cc:
            print("  WARNING: %s: no country for %s" % (sid, name))
        rows.append([int(sid), name, oid, cc, tp, ap, "openalex"])
    time.sleep(0.12)

found = {str(r[0]) for r in rows}
superseded = sorted({str(r[0]) for r in manual} & found, key=int)
manual = [r for r in manual if str(r[0]) not in found]
all_rows = sorted(rows + manual, key=lambda r: (int(r[0]), str(r[1])))
by_study = {}
for r in all_rows:
    by_study.setdefault(str(r[0]), []).append(r)
uncovered = [sid for sid, _, _ in studies if sid not in by_study]
unmapped = sorted({"%s (%s)" % (r[1], r[4]) for r in all_rows if not category(r[1], r[4], r[5])})
unpinned_manual = sorted({str(r[0]) for r in all_rows if str(r[6]).startswith("manual")} - set(missing) - pinned, key=int)

print("%d studies; OpenAlex gave institutions for %d; %d institution rows; %d manual rows kept"
      % (len(studies), len(found), len(rows), len(manual)))
print("no OpenAlex institutions:", missing, "| still uncovered after manual rows:", uncovered)
if superseded:
    print("manual rows dropped because OpenAlex now has the study:", superseded)
if errors:
    print("errors:", errors)
if unmapped:
    print("institutions with no category in lookups.json (add to institution_type_overrides):", unmapped)
if unpinned_manual:
    print("WARNING: manual rows for studies OpenAlex also covers; pin or remove them:", unpinned_manual)
print("rows that are sub-units of a university, counted as academic: %d"
      % sum(1 for r in all_rows if r[5] and r[1] not in LK["institution_type_overrides"]))
if DRY:
    sys.exit(0)

if SHEET in wb.sheetnames:
    del wb[SHEET]
ws = wb.create_sheet(SHEET)
ws.append(COLS)
for r in all_rows:
    ws.append(r)

# refresh the derived Studies columns
for ri in range(2, st.max_row + 1):
    sid = st.cell(ri, col["study_id"] + 1).value
    if sid is None or str(sid) not in by_study:
        continue
    rs = by_study[str(sid)]
    cs = sorted({r[3] for r in rs if r[3]})
    cats = {category(r[1], r[4], r[5]) for r in rs}
    afr, non = any(c in AFRICA for c in cs), any(c not in AFRICA for c in cs)
    vals = {"n_institutions": len(rs), "inst_countries": "; ".join(cs),
            "collab_breadth": ("Multi-country" if len(cs) >= 2 else
                               "Multi-institution, single-country" if len(rs) >= 2 else "Single-institution"),
            "has_african_inst": "Yes" if afr else "No",
            "african_leadership": ("African-only" if afr and not non else
                                   "North-South" if afr and non else "Non-African-only"),
            "cross_sector": "Yes" if "Academic" in cats and any(c != "Academic" for c in cats if c) else "No"}
    for k, v in vals.items():
        st.cell(ri, col[k] + 1).value = v
wb.save(WB)
print("wrote sheet %s and refreshed the Studies affiliation columns in %s" % (SHEET, WB.name))
