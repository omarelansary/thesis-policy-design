#!/usr/bin/env python3
"""Sanctioned, hash-verified, read-only access to evidence, with provenance.

Why this exists: direct reads of the research repository are blocked in this workspace (settings + hook).
This tool is the one route to (a) stored source texts and (b) a small allow-listed set of origin records.
It never writes to the origin. It verifies SHA-256 before reading and, unless --no-write, stores the passage as
an extract record (evidence/extracts/EXT-NNNN.md) that can be re-verified later by tools/verify_workspace.py.

Usage
  python tools/origin_extract.py --source <source-id> --lines 120-160 [--note "why"] [--no-write]
  python tools/origin_extract.py --governing <path under evidence/governing> --lines 5-18 [--note ...] [--no-write]
  python tools/origin_extract.py --origin-path <origin-relative path> --lines 7-48 [--note ...]      (allow-list only)
  python tools/origin_extract.py --list-sources [--grep TEXT]
Line numbers are 1-based and inclusive, counted on the text split by line breaks.
"""
import argparse, datetime, hashlib, json, os, pathlib, sys

WS = pathlib.Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def load_json(p):
    return json.loads((WS / p).read_text(encoding="utf-8"))


def read_lines(path, a, b):
    raw = pathlib.Path(path).read_bytes()
    text = raw.decode("utf-8")
    lines = text.splitlines()
    if a < 1 or b < a or b > len(lines):
        sys.exit(f"ERROR: line range {a}-{b} outside 1-{len(lines)}")
    return raw, lines[a - 1:b], len(lines)


def next_id():
    d = WS / "evidence" / "extracts"
    d.mkdir(parents=True, exist_ok=True)
    n = 1
    while True:
        p = d / f"EXT-{n:04d}.md"
        try:
            fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)  # atomic reservation: no two agents share an id
            return n, p, fd
        except FileExistsError:
            n += 1


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--source")
    g.add_argument("--governing")
    g.add_argument("--origin-path")
    g.add_argument("--list-sources", action="store_true")
    ap.add_argument("--lines")
    ap.add_argument("--note", default="")
    ap.add_argument("--grep", default="")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()

    origin = load_json("config/origin.json")
    root = pathlib.Path(origin["origin_path"])

    if a.list_sources:
        for s in load_json("evidence/sources.json")["sources"]:
            line = f'{s["id"]}\t{s["retrieved_at_utc"]}\t{s["input"]}'
            if a.grep.lower() in line.lower():
                print(line)
        return
    if not a.lines or "-" not in a.lines:
        sys.exit("ERROR: --lines START-END required")
    lo, hi = (int(x) for x in a.lines.split("-", 1))

    if a.source:
        meta = next((s for s in load_json("evidence/sources.json")["sources"] if s["id"] == a.source), None)
        if not meta:
            sys.exit(f"ERROR: unknown source id {a.source} (see --list-sources)")
        if not meta.get("has_text"):
            sys.exit(f"ERROR: source {a.source} has no stored text ({meta.get('kind')}).")
        path = root / meta["origin_text_path"]
        kind, sid, spath = "stored-source", a.source, meta["origin_text_path"]
        expect = meta["text_sha256_recomputed"]
        extra = {"source_url": meta["input"], "source_retrieved_at_utc": meta["retrieved_at_utc"],
                 "manifest_text_sha256": meta["manifest_text_sha256"]}
    elif a.governing:
        idx = {f["path"]: f for f in load_json("evidence/governing/INDEX.json")["files"]}
        key = a.governing.replace("\\", "/").replace("evidence/governing/", "")
        if key not in idx:
            sys.exit(f"ERROR: not a governing copy: {key}")
        path = WS / idx[key]["copy"]
        kind, sid, spath = "governing-copy", key, idx[key]["copy"]
        expect = idx[key]["sha256"]
        extra = {"origin_git_blob12": idx[key]["origin_git_blob12"]}
    else:
        allow = load_json("config/extractable_origin.json")["allow"]
        key = a.origin_path.replace("\\", "/")
        rule = next((r for r in allow if r["path"] == key), None)
        if not rule:
            sys.exit(f"ERROR: {key} is not on the extractable-origin allow-list (config/extractable_origin.json). "
                     "Request human authorization to extend the list.")
        if not any(r0 <= lo and hi <= r1 for r0, r1 in rule["line_ranges"]):
            sys.exit(f"ERROR: lines {lo}-{hi} outside the allowed ranges {rule['line_ranges']} for {key}")
        path = root / key
        kind, sid, spath = "origin-record", key, key
        expect = rule["sha256"]
        extra = {"allow_reason": rule["reason"]}

    if not path.exists():
        sys.exit(f"ERROR: file not available: {path}")
    raw, sel, total = read_lines(path, lo, hi)
    got = sha256_bytes(raw)
    if got != expect:
        sys.exit(f"ERROR: SHA-256 mismatch for {sid}: expected {expect[:16]}..., got {got[:16]}... (source changed or manifest stale). Nothing extracted.")

    body = "\n".join(sel)
    if a.no_write:
        print(f"[view only; hash verified {got[:12]}; {kind} {sid} lines {lo}-{hi} of {total}]")
        print(body)
        return
    n, p, fd = next_id()
    ex_id = f"EXT-{n:04d}"
    fm = {
        "id": ex_id, "type": "extract", "verbatim": True, "source_kind": kind, "source_id": sid, "source_path": spath,
        "source_sha256": got, "origin_head": origin["origin_head"], "line_start": lo, "line_end": hi,
        "extracted_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "tool": "tools/origin_extract.py", "note": a.note, **extra,
    }
    head = "---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items()) + "\n---\n"
    content = head + "<<<BEGIN-VERBATIM\n" + body + "\nEND-VERBATIM>>>\n"
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"wrote evidence/extracts/{ex_id}.md  ({kind} {sid} lines {lo}-{hi}; hash verified {got[:12]})")


if __name__ == "__main__":
    main()
