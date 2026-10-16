#!/usr/bin/env python3
"""Verify the workspace state. Exit code 0 = no FAIL. Read-only (never writes, never touches the origin except to read hashes).

  python tools/verify_workspace.py            full check (re-verifies extracts and manifests against the origin if it is present)
  python tools/verify_workspace.py --quick    structure, settings, agents, hashes of local copies, record schemas; no origin access

What a PASS means: the checks below hold. It does not mean the science is right, and it cannot detect instruction-level
violations (for example an agent ignoring a rule that no hook or permission enforces). See ops/SAFEGUARDS.md.
"""
import argparse, hashlib, json, pathlib, re, subprocess, sys

WS = pathlib.Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
ap = argparse.ArgumentParser()
ap.add_argument("--quick", action="store_true")
args = ap.parse_args()
res = {"PASS": 0, "WARN": 0, "FAIL": 0}


def rep(level, msg):
    res[level] += 1
    if level != "PASS" or not args.quick:
        print(f"{level:4} {msg}")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def fm(path):
    """Minimal front-matter reader: 'key: value' lines between --- markers; values parsed as JSON when possible."""
    t = pathlib.Path(path).read_bytes().decode("utf-8")
    if not t.startswith("---"):
        return None, t
    end = t.find("\n---", 3)
    if end < 0:
        return None, t
    d = {}
    for line in t[3:end].strip().splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            v = v.strip()
            try:
                d[k.strip()] = json.loads(v)
            except Exception:
                d[k.strip()] = v
    return d, t[end + 4:]


def need(cond, ok, bad):
    rep("PASS" if cond else "FAIL", ok if cond else bad)
    return cond


# ---------- 1. required files ----------
for f in ["CLAUDE.md", ".claude/settings.json", "ops/STATE.md", "ops/AUTHORIZATIONS.md", "ops/PROTOCOL.md", "ops/RECORDS.md",
          "ops/SAFEGUARDS.md", "ops/DESIGN-DECISIONS.md", "config/origin.json", "config/ownership.json", "config/extractable_origin.json",
          "evidence/README.md", "evidence/CAVEATS.md", "evidence/sources.json", "evidence/origin-index.tsv", "evidence/restricted.json",
          "evidence/governing/INDEX.json", "requirements/REGISTER.md", "requirements/intake/README.md", "tools/guard.py",
          "tools/origin_extract.py", "tools/verify_workspace.py"]:
    need((WS / f).exists(), f"present: {f}", f"missing: {f}")

# ---------- 2. settings ----------
try:
    st = json.loads((WS / ".claude/settings.json").read_text(encoding="utf-8"))
    need(st.get("autoMemoryEnabled") is False, "auto memory disabled", "autoMemoryEnabled must be false")
    env = st.get("env", {})
    need(env.get("CLAUDE_CODE_SUBAGENT_MODEL") == "claude-sonnet-5-5" and env.get("CLAUDE_CODE_SUBAGENT_MODEL_FORCE") == "1",
         "subagent model pinned to claude-sonnet-5-5 (forced)", "subagent model pin missing")
    deny = " ".join(st.get("permissions", {}).get("deny", []))
    for needle in ["research-cleanroom/**", "thesis-backups", ".claude/projects", "git push", "git clone", "Skill(import-memory)", "mcp__claude_ai_Google_Drive"]:
        need(needle in deny, f"deny rule present: {needle}", f"deny rule missing: {needle}")
    hooks = json.dumps(st.get("hooks", {}))
    need("tools/guard.py" in hooks and '"onFailure": "block"' in hooks.replace('":"', '": "'), "guard hook configured (fail-closed)", "guard hook missing or not fail-closed")
except Exception as e:
    rep("FAIL", f"settings unreadable: {e}")

# ---------- 3. agents ----------
own = json.loads((WS / "config/ownership.json").read_text(encoding="utf-8"))["agents"]
names = []
for p in sorted((WS / ".claude/agents").glob("*.md")):
    d, _ = fm(p)
    if not d:
        rep("FAIL", f"agent {p.name}: no front matter")
        continue
    names.append(d.get("name"))
    tools = [t.strip() for t in str(d.get("tools", "")).split(",")]
    need(d.get("name") == p.stem, f"agent {p.stem}: name matches file", f"agent {p.stem}: name mismatch")
    need(d.get("model") == "claude-sonnet-5-5", f"agent {p.stem}: model claude-sonnet-5-5", f"agent {p.stem}: model is {d.get('model')}")
    need("SendMessage" in tools, f"agent {p.stem}: has SendMessage", f"agent {p.stem}: lacks SendMessage")
    need(not ({"Agent", "Task", "WebSearch", "WebFetch"} & set(tools)), f"agent {p.stem}: no spawn/web tools", f"agent {p.stem}: has spawn or web tools")
    need(d.get("name") in own, f"agent {p.stem}: ownership entry", f"agent {p.stem}: no ownership entry")
need(len(names) == len(own), f"{len(names)} agents == {len(own)} ownership entries", "agents and ownership entries differ")

# ---------- 4. governing copies and manifests ----------
idx = json.loads((WS / "evidence/governing/INDEX.json").read_text(encoding="utf-8"))
listed = set()
for f in idx["files"]:
    p = WS / f["copy"]
    listed.add(p.resolve())
    if not p.exists():
        rep("FAIL", f"governing copy missing: {f['copy']}")
    elif sha(p) != f["sha256"]:
        rep("FAIL", f"governing copy MODIFIED: {f['copy']}")
    else:
        rep("PASS", f"governing copy intact: {f['path']}")
extra = [p for p in (WS / "evidence/governing").rglob("*") if p.is_file() and p.name != "INDEX.json" and p.resolve() not in listed]
need(not extra, "no unindexed files under evidence/governing", f"unindexed files under evidence/governing: {[str(e.relative_to(WS)) for e in extra][:5]}")
src = json.loads((WS / "evidence/sources.json").read_text(encoding="utf-8"))
need(src["count"] == len(src["sources"]), f"sources.json count consistent ({src['count']})", "sources.json count mismatch")
need(all(s["manifest_text_sha256"] in (None, s["text_sha256_recomputed"]) for s in src["sources"] if s.get("has_text")), "sources.json: manifest and recomputed text hashes agree", "sources.json hash disagreement")
rj = json.loads((WS / "evidence/restricted.json").read_text(encoding="utf-8"))["withheld"]
bad = set(v["sha256"] for v in rj.values() if v["sha256"])
leak = []
for p in WS.rglob("*"):
    if p.is_file() and ".git" not in p.parts and p.stat().st_size < 5_000_000:
        if sha(p) in bad:
            leak.append(str(p.relative_to(WS)))
need(not leak, "no workspace file is a copy of a withheld origin file", f"WITHHELD FILE COPIED: {leak}")
big = [str(p.relative_to(WS)) for p in WS.rglob("*") if p.is_file() and ".git" not in p.parts and p.stat().st_size > 5_000_000]
need(not big, "no file over 5 MB", f"large files: {big}")

# ---------- 5. origin cross-check (full mode) ----------
origin = json.loads((WS / "config/origin.json").read_text(encoding="utf-8"))
op = pathlib.Path(origin["origin_path"])
if not args.quick:
    if op.exists():
        mism = 0
        withtext = [s for s in src["sources"] if s.get("has_text")]
        for s in withtext:
            t = op / s["origin_text_path"]
            if not t.exists() or sha(t) != s["text_sha256_recomputed"]:
                mism += 1
        need(mism == 0, f"all {len(withtext)} stored-source texts match the origin hashes ({src['count'] - len(withtext)} sources have no stored text)", f"{mism} stored-source hashes differ from the origin")
        try:
            head = subprocess.run(["git", "-C", str(op), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            rep("PASS" if head == origin["origin_head"] else "WARN",
                "origin HEAD unchanged since snapshot" if head == origin["origin_head"] else
                f"origin HEAD moved ({head[:12]} vs snapshot {origin['origin_head'][:12]}): the origin gained commits after the snapshot; governing copies may be stale")
        except Exception:
            rep("WARN", "could not read origin HEAD")
    else:
        rep("WARN", "origin repository not found: stored-source extracts cannot be re-verified")

# ---------- 6. records ----------
auth_text = (WS / "ops/AUTHORIZATIONS.md").read_text(encoding="utf-8")
auth_ids = set(re.findall(r"\bAUTH-\d{3}\b", auth_text))
ids = {}
for p in sorted((WS / "evidence/extracts").glob("EXT-*.md")):
    d, body = fm(p)
    if not d or d.get("type") != "extract":
        rep("FAIL", f"{p.name}: not a valid extract record")
        continue
    ids[d["id"]] = p
    m = re.search(r"<<<BEGIN-VERBATIM\n(.*)\nEND-VERBATIM>>>", body, re.S)
    if not m:
        rep("FAIL", f"{p.name}: verbatim markers missing")
        continue
    kind, sp = d["source_kind"], d["source_path"]
    path = WS / sp if kind == "governing-copy" else op / sp
    if not path.exists():
        rep("WARN", f"{d['id']}: source not available here ({kind}); verbatim body not re-verified")
        continue
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != d["source_sha256"]:
        rep("FAIL", f"{d['id']}: source hash changed since extraction")
        continue
    lines = raw.decode("utf-8").splitlines()[d["line_start"] - 1:d["line_end"]]
    need("\n".join(lines) == m.group(1), f"{d['id']}: verbatim body matches source lines {d['line_start']}-{d['line_end']}", f"{d['id']}: verbatim body DIFFERS from source")

TYPES = {"findings": ("finding", "FND"), "hypotheses": ("hypothesis", "HYP"), "design/proposals": ("design-proposal", "DPR"),
         "design/choices": ("design-choice", "DES"), "challenges": ("challenge", "CH"), "reviews": ("review", "RV")}
recs = []
for d_, (typ, pre) in TYPES.items():
    for p in sorted((WS / d_).glob("*.md")):
        if p.name.lower() == "readme.md":
            continue
        d, _ = fm(p)
        if not d:
            rep("FAIL", f"{d_}/{p.name}: missing front matter")
            continue
        recs.append((p, d, typ, pre))
        ok = d.get("type") == typ and str(d.get("id", "")).startswith(pre + "-") and d.get("status") and d.get("created_by") and d.get("created_utc")
        need(ok, f"{d_}/{p.name}: header ok ({d.get('id')})", f"{d_}/{p.name}: bad header (need type={typ}, id {pre}-*, status, created_by, created_utc)")
        if d.get("id") in ids:
            rep("FAIL", f"duplicate id {d.get('id')}")
        ids[d.get("id")] = p
reqs = set(re.findall(r"\bREQ-[A-Za-z0-9-]+\b", (WS / "requirements/REGISTER.md").read_text(encoding="utf-8")))
for p, d, typ, pre in recs:
    refs = []
    for k in ("evidence", "basis", "target"):
        v = d.get(k)
        refs += v if isinstance(v, list) else ([v] if isinstance(v, str) and v else [])
    for r in refs:
        r = str(r)
        if re.match(r"(EXT|FND|HYP|DPR|DES|CH|RV)-", r):
            need(r in ids, f"{p.name}: reference {r} resolves", f"{p.name}: dangling reference {r}")
        elif r.startswith("REQ-"):
            need(r in reqs, f"{p.name}: reference {r} resolves", f"{p.name}: unknown requirement {r}")
    if typ == "finding":
        need(any(str(r).startswith("EXT-") for r in refs), f"{p.name}: finding cites an extract", f"{p.name}: finding without EXT evidence")
    if typ == "hypothesis":
        need(bool(d.get("falsifier")), f"{p.name}: falsifier stated", f"{p.name}: hypothesis without falsifier")
    if d.get("status") == "approved":
        need(d.get("approved_by") == "human" and d.get("authorization") in auth_ids,
             f"{p.name}: approval cites human and an AUTH id", f"{p.name}: 'approved' without approved_by=human and a valid authorization id")

# ---------- 7. authorization register ----------
rows = [l for l in auth_text.splitlines() if re.match(r"\|\s*AUTH-\d{3}\s*\|", l)]
for l in rows:
    cells = [c.strip() for c in l.strip().strip("|").split("|")]
    need(len(cells) >= 6 and cells[3] and cells[5], f"{cells[0]}: has date and verbatim human quote", f"{cells[0]}: missing date or human quote")

# ---------- 8. git ----------
try:
    g = lambda *a: subprocess.run(["git", "-C", str(WS), *a], capture_output=True, text=True).stdout.strip()
    need(g("remote") == "", "no git remote configured", f"git remote present: {g('remote')}")
    dirty = [l for l in g("status", "--porcelain").splitlines()]
    rep("PASS" if not dirty else "WARN", "git working tree clean" if not dirty else f"{len(dirty)} uncommitted change(s)")
    print(f"INFO branch={g('rev-parse', '--abbrev-ref', 'HEAD')} head={g('rev-parse', '--short', 'HEAD')} mode={'quick' if args.quick else 'full'}")
except Exception as e:
    rep("WARN", f"git unavailable: {e}")

print(f"SUMMARY pass={res['PASS']} warn={res['WARN']} fail={res['FAIL']}")
sys.exit(1 if res["FAIL"] else 0)
