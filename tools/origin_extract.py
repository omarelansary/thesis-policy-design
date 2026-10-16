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
  python tools/origin_extract.py --intake-source <INT-id> --lines 12-30 [--note ...]                 (human-approved line ranges only)
  python tools/origin_extract.py --list-intake                       (ids, approved ranges, metadata; never content)
  python tools/origin_extract.py --describe-file <path>              (SHA-256, bytes, LF line count, mtime; never content)
Line numbers are 1-based and inclusive; a line ends at LF only (CR before LF is dropped), the same count as sed/grep -n.
(Python str.splitlines would also split at form feed and other characters; 7 stored sources contain such characters.)

--source accepts a manifest id, or a short name listed in config/source_aliases.json (the short names the governing documents use,
for example r4-github). An alias is resolved explicitly: the tool prints which manifest id it used and the extract records it as
`cited_as`. A name that denotes a family or is ambiguous is refused with the list of members. Nothing is ever resolved by silent prefix.

--intake-source (AUTH-002 item 2): supervisor or user material that lives OUTSIDE the workspace (for example a transcript that also
contains earlier-thesis experimental content) is admitted only through an entry in config/intake_sources.json that the human
authorized: it fixes the file's SHA-256 and the exact approved line ranges. The tool reads the whole file only to hash it and to
count lines; it writes only the requested lines, and refuses lines outside the approved ranges, a changed file, or a path in the
forbidden locations. Each extract records source identity, supplier, form, file modification time, location (line range),
the full-file SHA-256 and the SHA-256 of the extracted body. See requirements/intake/README.md.
"""
import argparse, datetime, hashlib, json, os, pathlib, re, sys

WS = pathlib.Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
FORBIDDEN = re.compile(  # same locations as tools/guard.py; this tool refuses them too because Python bypasses the hook
    r"research-clean|cleanroom|thesis-back|claude_forensic|forensic_rescue|"
    r"[\\/]\.claude[\\/](projects|history|file-history|plans|backups|session-env)", re.I)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def load_json(p):
    return json.loads((WS / p).read_text(encoding="utf-8"))


def read_lines(path, a, b):
    raw = pathlib.Path(path).read_bytes()
    text = raw.decode("utf-8")
    lines = text.split("\n")  # a line ends at LF only (as sed, grep -n and editors count); form feed etc. are NOT line breaks
    if lines and lines[-1] == "":
        lines.pop()
    lines = [l[:-1] if l.endswith("\r") else l for l in lines]
    if a < 1 or b < a or b > len(lines):
        sys.exit(f"ERROR: line range {a}-{b} outside 1-{len(lines)}")
    return raw, lines[a - 1:b], len(lines)


def resolve_source(name, sources):
    """Manifest id for a name: exact id, else an explicit alias from config/source_aliases.json, else an error with hints."""
    by = {s["id"]: s for s in sources}
    if name in by:
        return by[name], None
    al = load_json("config/source_aliases.json") if (WS / "config/source_aliases.json").exists() else {"aliases": {}, "groups": {}}
    if name in al["aliases"]:
        a = al["aliases"][name]
        return by[a["id"]], f"alias '{name}' -> manifest id {a['id']} ({a['basis']})"
    if name in al["groups"]:
        g = al["groups"][name]
        sys.exit(f"ERROR: '{name}' is not one source: {g['basis']}. Members: " + ", ".join(g["members"]))
    near = [i for i in by if i.startswith(name)][:8]
    sys.exit(f"ERROR: unknown source id {name} (see --list-sources)" + (f". Manifest ids starting with it: {', '.join(near)}" if near else ""))


def describe(path):
    p = pathlib.Path(path)
    if FORBIDDEN.search(str(p)):
        sys.exit("ERROR: that location is not available to this workspace.")
    if not p.is_file():
        sys.exit(f"ERROR: not a file: {p}")
    raw = p.read_bytes()
    text = raw.decode("utf-8")
    n = len(text.split("\n")) - (1 if text.endswith("\n") else 0)
    mt = datetime.datetime.fromtimestamp(p.stat().st_mtime, datetime.timezone.utc).isoformat(timespec="seconds")
    return sha256_bytes(raw), len(raw), n, mt


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
    g.add_argument("--intake-source")
    g.add_argument("--list-intake", action="store_true")
    g.add_argument("--describe-file")
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
    if a.list_intake:
        ents = load_json("config/intake_sources.json")["sources"] if (WS / "config/intake_sources.json").exists() else []
        if not ents:
            print("no intake sources registered")
        for e in ents:
            print(f'{e["id"]}\tauthorization={e["authorization"]}\tranges={e["allowed_ranges"]}\tsupplied_by={e["supplied_by"]}\t'
                  f'{e["supplied_utc"]}\t{e["form"]}\t{e["source_identity"]}')
        return
    if a.describe_file:
        h, nbytes, nlines, mt = describe(a.describe_file)
        print(f"sha256={h}\nbytes={nbytes}\nlines={nlines}\nmtime_utc={mt}")
        return
    if not a.lines or "-" not in a.lines:
        sys.exit("ERROR: --lines START-END required")
    lo, hi = (int(x) for x in a.lines.split("-", 1))

    if a.source:
        meta, note = resolve_source(a.source, load_json("evidence/sources.json")["sources"])
        if note:
            print(f"[{note}]")
        if not meta.get("has_text"):
            sys.exit(f"ERROR: source {meta['id']} has no stored text ({meta.get('kind')}).")
        path = root / meta["origin_text_path"]
        kind, sid, spath = "stored-source", meta["id"], meta["origin_text_path"]
        expect = meta["text_sha256_recomputed"]
        extra = {"source_url": meta["input"], "source_retrieved_at_utc": meta["retrieved_at_utc"],
                 "manifest_text_sha256": meta["manifest_text_sha256"]}
        if a.source != meta["id"]:
            extra["cited_as"] = a.source
    elif a.intake_source:
        cfg = load_json("config/intake_sources.json") if (WS / "config/intake_sources.json").exists() else {"sources": []}
        ent = next((e for e in cfg["sources"] if e["id"] == a.intake_source), None)
        if not ent:
            sys.exit(f"ERROR: {a.intake_source} is not registered in config/intake_sources.json. The human must authorize the file and its line ranges first (requirements/intake/README.md).")
        auths = set(re.findall(r"\bAUTH-\d{3}\b", (WS / "ops/AUTHORIZATIONS.md").read_text(encoding="utf-8")))
        if ent["authorization"] not in auths or ent["authorization"] in ("AUTH-001", "AUTH-002"):
            sys.exit(f"ERROR: intake entry {ent['id']} cites {ent['authorization']}, which is not an authorization of this extract (AUTH-001/002 cover the mechanism only).")
        if not any(r0 <= lo and hi <= r1 for r0, r1 in ent["allowed_ranges"]):
            sys.exit(f"ERROR: lines {lo}-{hi} are outside the approved ranges {ent['allowed_ranges']} of {ent['id']}. Nothing read for output.")
        path = pathlib.Path(ent["path"])
        if FORBIDDEN.search(str(path)):
            sys.exit("ERROR: that location is not available to this workspace.")
        kind, sid, spath = "intake-source", ent["id"], str(path)
        expect = ent["sha256"]
        extra = {k: ent[k] for k in ("authorization", "supplied_by", "supplied_utc", "form", "source_identity", "stated_nature") if k in ent}
        for k in ("locator_note", "caveats"):
            if ent.get(k):
                extra[k] = ent[k]
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
        "source_sha256": got, "source_total_lines": total, "line_start": lo, "line_end": hi,
        "body_sha256": sha256_bytes(body.encode("utf-8")),
        "extracted_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "tool": "tools/origin_extract.py", "note": a.note, **extra,
    }
    if kind == "intake-source":
        fm["source_file_mtime_utc"] = datetime.datetime.fromtimestamp(path.stat().st_mtime, datetime.timezone.utc).isoformat(timespec="seconds")
    else:
        fm["origin_head"] = origin["origin_head"]
    head = "---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items()) + "\n---\n"
    content = head + "<<<BEGIN-VERBATIM\n" + body + "\nEND-VERBATIM>>>\n"
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"wrote evidence/extracts/{ex_id}.md  ({kind} {sid} lines {lo}-{hi}; hash verified {got[:12]})")


if __name__ == "__main__":
    main()
