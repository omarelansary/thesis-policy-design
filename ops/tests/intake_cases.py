"""AUTH-002 regression: intake mechanism and source-alias resolution, with SYNTHETIC content only (no supervisor material).
Works in throwaway copies of the workspace; the synthetic 'original' lives in a temp directory.
Run: python ops/tests/intake_cases.py   (exit 1 if any case fails)"""
import hashlib, json, pathlib, re, shutil, subprocess, sys, tempfile

SRC = pathlib.Path(__file__).resolve().parents[2]
bad = 0
PY = sys.executable


def fresh():
    root = pathlib.Path(tempfile.mkdtemp(prefix="tpd-intake-"))
    d = root / "thesis-policy-design"
    # this file is left out of the copy: it contains the synthetic 'excluded' lines, which the leak detector would (rightly) flag
    shutil.copytree(SRC, d, ignore=shutil.ignore_patterns(".git", "raw", "__pycache__", "intake_cases.py"))
    return root, d


def sh(d, *args):
    r = subprocess.run([PY, *args], capture_output=True, text=True, encoding="utf-8", cwd=d)
    return r.returncode, r.stdout + r.stderr


def ok(name, cond, detail=""):
    global bad
    bad += not cond
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else "   " + detail[:300]))


# synthetic original: lines 1-4 approved, lines 5-8 'excluded' (long, distinctive), line 9 approved
LINES = ["SYN-HEADER synthetic transcript, not real", "Supervisor: synthetic requirement one, stated plainly here.", "Student: synthetic question.",
         "Supervisor: synthetic requirement two, stated plainly here.",
         "EXCLUDED-SYNTHETIC line five that stands for earlier experimental results, long enough to be matched",
         "EXCLUDED-SYNTHETIC line six that stands for more earlier experimental results, long enough too",
         "EXCLUDED-SYNTHETIC line seven, again a long distinctive sentence about another earlier result",
         "EXCLUDED-SYNTHETIC line eight, final long distinctive sentence about the earlier results",
         "Supervisor: synthetic closing remark that is approved for admission."]


def setup(authorized=True, auth_id="AUTH-777"):
    root, d = fresh()
    orig = root / "original.txt"
    orig.write_bytes(("\n".join(LINES) + "\n").encode("utf-8"))
    h = hashlib.sha256(orig.read_bytes()).hexdigest()
    entry = {"id": "INT-001", "path": str(orig), "sha256": h, "total_lines": len(LINES), "allowed_ranges": [[1, 4], [9, 9]],
             "authorization": auth_id, "supplied_by": "synthetic", "supplied_utc": "2026-01-01T00:00:00+00:00", "form": "transcript",
             "source_identity": "synthetic file original.txt", "stated_nature": "synthetic test input"}
    (d / "config/intake_sources.json").write_text(json.dumps({"note": "t", "sources": [entry]}), encoding="utf-8")
    if authorized:
        a = d / "ops/AUTHORIZATIONS.md"
        a.write_text(a.read_text(encoding="utf-8") + f"\n| {auth_id} | human | synthetic | 2026-01-01 | none | \"synthetic quote\" |\n", encoding="utf-8")
    sh(d, "tools/verify_workspace.py", "--repin")  # the throwaway copy's own pin, so only the behaviour under test can fail
    return root, d, orig, entry


def verify(d):
    return sh(d, "tools/verify_workspace.py", "--quick")


def fails(out):
    return [l for l in out.splitlines() if l.startswith("FAIL")]


# 1. approved range extracts, with provenance fields
root, d, orig, e = setup()
try:
    c, out = sh(d, "tools/origin_extract.py", "--intake-source", "INT-001", "--lines", "2-4", "--note", "synthetic")
    ok("approved range 2-4 is extracted", c == 0 and "wrote evidence/extracts/" in out, out)
    ext = next((p for p in sorted((d / "evidence/extracts").glob("EXT-*.md")) if "INT-001" in p.read_text(encoding="utf-8")), None)
    t = ext.read_text(encoding="utf-8") if ext else ""
    ok("extract records identity, location, full-file hash, body hash, mtime, supplier, authorization",
       all(k in t for k in ('source_kind: "intake-source"', "line_start: 2", "line_end: 4", e["sha256"], "body_sha256:", "source_file_mtime_utc:", 'supplied_by: "synthetic"', 'authorization: "AUTH-777"', "source_total_lines: 9")), t[:600])
    ok("extract body is verbatim and contains no excluded text", "synthetic requirement two" in t and "EXCLUDED-SYNTHETIC" not in t)
    c, out = verify(d)
    ok("verify passes with the extract present", c == 0 and not fails(out), str(fails(out)))
    # 2. change detection
    raw_t = ext.read_bytes()
    ext.write_bytes(raw_t.replace(b"requirement two", b"requirement TWO", 1))
    c, out = verify(d)
    ok("edited extract body detected", c != 0 and any("body_sha256" in l or "DIFFERS" in l for l in fails(out)), str(fails(out)))
    ext.write_bytes(raw_t)
    orig.write_bytes(orig.read_bytes() + b"extra\n")
    c, out = verify(d)
    ok("changed original file detected", c != 0 and any("CHANGED" in l or "source hash changed" in l for l in fails(out)), str(fails(out)))
    orig.write_bytes(("\n".join(LINES) + "\n").encode("utf-8"))
    c, out = verify(d)
    ok("restoring the original clears the failure", c == 0 and not fails(out), str(fails(out)))
    # 3. leak of excluded text
    (d / "findings").mkdir(exist_ok=True)
    (d / "findings/leak.txt").write_text("note: " + LINES[5] + "\n", encoding="utf-8")
    c, out = verify(d)
    ok("excluded line copied into the workspace detected", c != 0 and any("EXCLUDED original text appears" in l for l in fails(out)), str(fails(out)))
    (d / "findings/leak.txt").unlink()
    (d / "findings/whole.txt").write_bytes(orig.read_bytes())
    c, out = verify(d)
    ok("whole original copied into the workspace detected", c != 0 and any("COPIED" in l for l in fails(out)), str(fails(out)))
finally:
    shutil.rmtree(root, ignore_errors=True)

# 4. refusals
root, d, orig, e = setup()
try:
    for rng, name in (("5-6", "range wholly outside"), ("4-5", "range straddling the boundary"), ("1-9", "range spanning excluded lines")):
        c, out = sh(d, "tools/origin_extract.py", "--intake-source", "INT-001", "--lines", rng)
        ok(f"{name} refused, nothing written", c != 0 and "approved ranges" in out and not list((d / "evidence/extracts").glob("EXT-0007.md")) and "EXCLUDED" not in out, out)
    c, out = sh(d, "tools/origin_extract.py", "--intake-source", "INT-999", "--lines", "1-2")
    ok("unregistered intake id refused", c != 0 and "not registered" in out, out)
    orig.write_bytes(orig.read_bytes() + b"x\n")
    c, out = sh(d, "tools/origin_extract.py", "--intake-source", "INT-001", "--lines", "1-2")
    ok("changed original refused by the tool", c != 0 and "SHA-256 mismatch" in out, out)
    c, out = sh(d, "tools/origin_extract.py", "--describe-file", str(orig))
    ok("--describe-file prints hash and counts, no content", c == 0 and "sha256=" in out and "lines=" in out and "SYN-HEADER" not in out, out)
    c, out = sh(d, "tools/origin_extract.py", "--describe-file", r"C:\Users\omr\Documents\research-cleanroom\CLAUDE.md")
    ok("--describe-file refuses a forbidden location by name", c != 0 and "not available" in out, out)
finally:
    shutil.rmtree(root, ignore_errors=True)

# 5. authorization binding
for auth, name in (("AUTH-002", "entry citing AUTH-002"), ("AUTH-001", "entry citing AUTH-001")):
    root, d, orig, e = setup(authorized=True, auth_id=auth)
    try:
        c, out = sh(d, "tools/origin_extract.py", "--intake-source", "INT-001", "--lines", "1-2")
        ok(f"tool refuses {name}", c != 0 and "not an authorization of this extract" in out, out)
        c, out = verify(d)
        ok(f"verify flags {name}", c != 0 and any("AUTH-001/002" in l for l in fails(out)), str(fails(out)))
    finally:
        shutil.rmtree(root, ignore_errors=True)
root, d, orig, e = setup(authorized=False)
try:
    c, out = sh(d, "tools/origin_extract.py", "--intake-source", "INT-001", "--lines", "1-2")
    ok("tool refuses an authorization id absent from the register", c != 0 and "not an authorization" in out, out)
finally:
    shutil.rmtree(root, ignore_errors=True)

# 6. direct-text intake records
root, d = fresh()
try:
    body = "synthetic pasted text"
    rec = ('---\ntype: "intake-text"\nsupplied_by: "synthetic"\nsupplied_utc: "2026-01-01T00:00:00+00:00"\nform: "message"\nstated_nature: "synthetic"\n'
           f'body_sha256: "{hashlib.sha256(body.encode()).hexdigest()}"\n---\n<<<BEGIN-VERBATIM\n{body}\nEND-VERBATIM>>>\n')
    p = d / "requirements/intake/2026-01-01-synthetic.md"
    p.write_bytes(rec.encode("utf-8"))
    c, out = verify(d)
    ok("valid intake-text record passes", c == 0 and not fails(out), str(fails(out)))
    p.write_bytes(rec.replace("pasted", "PASTED").encode("utf-8"))
    c, out = verify(d)
    ok("edited intake-text record detected", c != 0 and any("CHANGED" in l for l in fails(out)), str(fails(out)))
finally:
    shutil.rmtree(root, ignore_errors=True)

# 7. source aliases (real workspace, read-only)
def ex(*a):
    return sh(SRC, "tools/origin_extract.py", *a, "--no-write")


c, out = ex("--source", "r4-github", "--lines", "416-416")
ok("alias r4-github opens its manifest id and says so", c == 0 and "alias 'r4-github' -> manifest id r4-github-copilot-fewer-tools" in out and "27.5% absolute" in out, out)
c, out = ex("--source", "r4-github-copilot-fewer-tools", "--lines", "414-414")
ok("exact manifest id still works, no alias notice", c == 0 and "alias" not in out, out)
c, out = ex("--source", "r4-speakeasy", "--lines", "135-135")
ok("alias with two candidates resolves to the one with stored text", c == 0 and "toolsets2" in out, out)
c, out = ex("--source", "s4f-2b", "--lines", "1-1")
ok("family name refused with members listed", c != 0 and "not one source" in out and "s4f-2b-ntilc-2606-06566" in out, out)
c, out = ex("--source", "r4-gith", "--lines", "1-1")
ok("a mere prefix is not resolved silently; hints shown", c != 0 and "unknown source id" in out and "r4-github-copilot-fewer-tools" in out, out)
al = json.loads((SRC / "config/source_aliases.json").read_text(encoding="utf-8"))
ledger = (SRC / "evidence/governing/stage-reports/STAGE3_CLAIM_LEDGER-20261013.md").read_text(encoding="utf-8")
names = set(re.findall(r"\b(r[0-9]-[a-z0-9-]*[a-z0-9]|s[0-9][a-z]?-[a-z0-9-]*[a-z0-9]|ch-s2-\d{4})\b", ledger))
ids = {s["id"] for s in json.loads((SRC / "evidence/sources.json").read_text(encoding="utf-8"))["sources"]}
unres = sorted(n for n in names if n not in ids and n not in al["aliases"] and n not in al["groups"])
ok("every source-like name in the Stage 3 claim ledger resolves (id, alias or group)", not unres, str(unres))
print(f"failures {bad}")
sys.exit(1 if bad else 0)
