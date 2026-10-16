#!/usr/bin/env python3
"""BOOTSTRAP-ONLY: build the evidence-access layer from the research repository, read-only.

Reads the origin repository (never writes to it) and produces, inside this workspace:
  config/origin.json                origin path, HEAD commit, snapshot time
  evidence/sources.json             neutral manifest of ALL stored source texts (no selection)
  evidence/origin-index.tsv         inventory of tracked origin files (path, category, size, blob id, last commit, access)
  evidence/restricted.json          withheld origin files: reason + sha256 of their bytes (so copies can be detected)
  evidence/governing/INDEX.json     byte-exact copies of the governing records, with hashes and origin blob ids
  evidence/governing/<origin path>  the copies themselves

Selection rule for governing copies is written in evidence/README.md (rule-based, not claim-based).
Usage: python tools/build_origin_snapshot.py [--origin PATH]   (re-running overwrites generated files only)
"""
import argparse, datetime, hashlib, json, pathlib, shutil, subprocess, sys

WS = pathlib.Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("--origin", default=r"C:\Users\omr\Documents\research-cleanroom")
args = ap.parse_args()
ORIGIN = pathlib.Path(args.origin)


def git(*a):
    return subprocess.run(["git", "-C", str(ORIGIN), *a], capture_output=True, text=True, encoding="utf-8", errors="replace", check=True).stdout


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
head = git("rev-parse", "HEAD").strip()
head_date = git("log", "-1", "--format=%aI").strip()
dirty = [l for l in git("status", "--porcelain").splitlines() if not l.startswith("??")]

# ---- governing set (selection rule in evidence/README.md) ----
GOVERNING = {
    "approved brief and user decisions of the clean-room project": [
        "stage-reports/STAGE1_RESEARCH_BRIEF.md",
    ],
    "decision history (all decision records)": sorted(
        str(p.relative_to(ORIGIN)).replace("\\", "/") for p in (ORIGIN / "decisions").glob("*.md")),
    "latest candidate state, corrections and selection-ready evidence": [
        "stage-reports/S4G-SELECTION-READY-BRIEF-20261015.md",
        "candidate-questions/S4I-GOVERNING-ERRATUM-20261016.md",
        "stage-reports/S4I-SELECTION-DECISION-SHEET-20261016.md",
        "candidate-questions/S4D-CANDIDATE-DOSSIER-20261014.md",
        "candidate-questions/S4D-DEPENDENCY-MATRIX-20261014.md",
        "candidate-questions/S4D-QUALITY-ADDENDUM-20261014.md",
        "candidate-questions/S4F-UNCERTAINTY-ADDENDUM-20261015.md",
        "stage-reports/S4E-DECISION-READINESS-REPORT-20261015.md",
        "stage-reports/S4F-PRIOR-ART-ASSESSMENT-20261015.md",
        "stage-reports/S4F-VEHICLE-FEASIBILITY-REPORT-20261015.md",
    ],
    "final evidence syntheses per stage": [
        "stage-reports/STAGE2_FINAL_LANDSCAPE_REPORT-20261012.md",
        "stage-reports/STAGE3_FINAL_REPORT-20261013.md",
        "stage-reports/STAGE3_CLAIM_LEDGER-20261013.md",
        "stage-reports/STAGE4_PRIOR_ART_COMPARISON-20261013.md",
        "stage-reports/STAGE4B_OPPORTUNITY_MAP-20261013.md",
        "stage-reports/STAGE4B_FINAL_SYNTHESIS_AND_SUPERVISOR_ALIGNMENT-20261013.md",
        "stage-reports/STAGE4C_DECISION_EVIDENCE_DOSSIER-20261013.md",
    ],
    "audit and correction provenance": [
        "integrity-investigation-20261015/FINAL-REPORT-20261015.md",
        "audit-s4h-20261015/B2-REPORT.md",
        "audit-s4h-20261015/B1-source-version-report.md",
        "s4h-closure-20261016/S4H-CLOSURE-ADDENDUM.md",
    ],
}

RESTRICTED = {
    "inputs/stage1/supervisor-transcript-2026-10-02.md": "Personal, unpublished meeting transcript; contains student-reported prior-thesis results that remain outside the clean-room boundary. Its requirements are carried only through the approved brief and the meeting-record extracts (with transcript line references).",
    "stage-reports/STAGE1_MEETING_RECORD.md": "Section 3 (lines 50-66) records student-reported prior-thesis work. Only sections 1 and 2 (lines 7-48) are available, as extracts made with tools/origin_extract.py.",
    "evidence/S1-supervisor-meeting-2026-10-02.md": "Source record of the personal transcript (private document identifier, access details). Only its SHA-256 of the transcript text is carried in evidence/README.md.",
}

# ---- git inventory ----
ls = git("ls-tree", "-r", "-l", "HEAD").splitlines()
dates = {}
cur = None
for line in git("log", "--name-only", "--format=@@%aI", "--diff-filter=AMR").splitlines():
    if line.startswith("@@"):
        cur = line[2:]
    elif line.strip() and line not in dates:
        dates[line] = cur


def category(path):
    top = path.split("/")[0]
    return {
        "stage-reports": "stage-report", "candidate-questions": "candidate-record", "decisions": "decision-record",
        "audits": "audit-critic-worker-record", "searches": "search-log", "protocols": "protocol",
        "probes": "probe-output", "infrastructure": "tooling", "checkpoints": "operational-checkpoint",
        ".claude": "origin-agent-config", "integrity-investigation-20261015": "audit-record", "audit-s4h-20261015": "audit-record",
        "s4h-closure-20261016": "audit-record", "inputs": "restricted-input", "evidence": "evidence",
    }.get(top, "root-file")


gov_paths = {p for v in GOVERNING.values() for p in v}
rows, collapsed = [], {}
for l in ls:
    meta, path = l.split("\t", 1)
    mode, typ, blob, size = meta.split()
    if path.startswith("evidence/source-text/") or path.startswith("checkpoints/"):
        key = "/".join(path.split("/")[:3]) if path.startswith("evidence/source-text/") else "checkpoints"
        c = collapsed.setdefault(key, [0, 0])
        c[0] += 1
        c[1] += int(size)
        continue
    access = "restricted" if path in RESTRICTED else ("copied" if path in gov_paths else "indexed-only")
    rows.append((path, category(path), size, blob[:12], (dates.get(path) or "")[:10], access))

# ---- sources.json (all stored texts, neutral) ----
sources = []
for d in sorted((ORIGIN / "evidence" / "source-text").iterdir()):
    mf = d / "manifest.json"
    if not d.is_dir() or not mf.exists():
        continue
    m = json.loads(mf.read_text(encoding="utf-8-sig"))
    tp = d / "text.txt"
    sources.append({
        "id": d.name, "input": m.get("input"), "final_url": m.get("final_url"), "http_status": m.get("http_status"),
        "retrieved_at_utc": m.get("retrieved_at_utc"), "last_modified": m.get("last_modified"),
        "content_type": m.get("content_type"), "page_count": m.get("page_count"),
        "extractor": m.get("extractor"), "warnings": m.get("warnings") or [],
        "manifest_text_sha256": m.get("text_sha256"), "manifest_source_sha256": m.get("source_sha256"),
        "text_sha256_recomputed": sha256_file(tp) if tp.exists() else None,
        "text_bytes": tp.stat().st_size if tp.exists() else None,
        "origin_text_path": f"evidence/source-text/{d.name}/text.txt",
        "has_text": tp.exists(),
        "kind": ("fetch-tool test artefact (not research material)" if d.name.startswith("test-") else
                 ("fetch failed: no text stored" if not tp.exists() else "stored text")),
    })

# ---- write generated files ----
(WS / "config").mkdir(exist_ok=True)
(WS / "evidence" / "governing").mkdir(parents=True, exist_ok=True)
(WS / "config" / "origin.json").write_text(json.dumps({
    "origin_path": str(ORIGIN), "origin_head": head, "origin_head_date": head_date,
    "origin_tracked_files_dirty": dirty, "snapshot_utc": now,
    "note": "The origin repository remains authoritative for its historical records. This workspace never writes to it.",
}, indent=2), encoding="utf-8", newline="\n")
(WS / "evidence" / "sources.json").write_text(json.dumps({
    "origin_head": head, "snapshot_utc": now, "count": len(sources),
    "note": "Complete list of stored source texts. Metadata only: no selection, no ranking, no relevance judgement.",
    "sources": sources}, indent=1), encoding="utf-8", newline="\n")
with open(WS / "evidence" / "origin-index.tsv", "w", encoding="utf-8", newline="\n") as f:
    f.write("path\tcategory\tbytes\tgit_blob12\tlast_commit_date\taccess\n")
    for r in sorted(rows):
        f.write("\t".join(r) + "\n")
    for k, (n, s) in sorted(collapsed.items()):
        f.write(f"{k}/\tcollapsed-directory({n} files)\t{s}\t\t\tindexed-only\n")
restricted = {}
for p, why in RESTRICTED.items():
    fp = ORIGIN / p
    restricted[p] = {"reason": why, "sha256": sha256_file(fp) if fp.exists() else None}
(WS / "evidence" / "restricted.json").write_text(json.dumps({"origin_head": head, "withheld": restricted}, indent=2), encoding="utf-8", newline="\n")

index = {"origin_head": head, "snapshot_utc": now, "files": []}
for why, paths in GOVERNING.items():
    for p in paths:
        src = ORIGIN / p
        dst = WS / "evidence" / "governing" / p
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        index["files"].append({
            "path": p, "copy": f"evidence/governing/{p}", "selection_class": why,
            "sha256": sha256_file(dst), "bytes": dst.stat().st_size,
            "origin_git_blob12": git("rev-parse", f"HEAD:{p}").strip()[:12],
            "origin_last_commit_date": git("log", "-1", "--format=%aI", "--", p).strip(),
        })
(WS / "evidence" / "governing" / "INDEX.json").write_text(json.dumps(index, indent=1), encoding="utf-8", newline="\n")
print("origin head", head[:12], "| sources", len(sources), "| index rows", len(rows) + len(collapsed), "| governing copies", len(index["files"]), "| restricted", len(restricted))
