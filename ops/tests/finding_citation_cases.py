"""AUTH-022 regression: a finding may cite stored literature listed in evidence/literature-20261019/MANIFEST.jsonl (verify_workspace.py).
SYNTHETIC content only. Runs the verifier in a throwaway copy of the workspace whose literature folder and findings folder are replaced
by fixtures, then reads only the lines that name the fixture findings.
Run: python ops/tests/finding_citation_cases.py   (exit 1 if any case fails)"""
import hashlib, json, pathlib, shutil, subprocess, sys, tempfile

SRC = pathlib.Path(__file__).resolve().parents[2]
root = pathlib.Path(tempfile.mkdtemp(prefix="tpd-findcite-"))
WS = root / "thesis-policy-design"
shutil.copytree(SRC, WS, ignore=shutil.ignore_patterns(".git", "raw", "__pycache__", "literature-20261019", "findings", "intake_cases.py", "finding_citation_cases.py"))
LIT = WS / "evidence" / "literature-20261019"
LIT.mkdir(parents=True)
(WS / "findings").mkdir()

rows = []


def lit(file_name, text, manifest_id=None, tamper=None, delete=False, listed=True):
    """Store a fixture literature file; the manifest records the hash of `text`; `tamper` replaces the stored bytes afterwards."""
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    (LIT / file_name).write_text(tamper if tamper is not None else text, encoding="utf-8", newline="\n")
    if delete:
        (LIT / file_name).unlink()
    if listed:
        rows.append({"id": manifest_id or file_name.rsplit(".", 1)[0], "url": "https://example.invalid/" + file_name, "http": "200", "kind": "html",
                     "text_sha256": h, "raw_sha256": h, "text_lines": 1, "auth": "AUTH-013"})


lit("ok-a.txt", "alpha\n")
lit("ok-b.txt", "beta\n")
lit("raw-c.csv", "a,b\n1,2\n", manifest_id="raw-c.csv")      # manifest id already carries the extension
lit("tampered.txt", "original\n", tamper="changed\n")         # bytes differ from the recorded hash
lit("gone.txt", "was here\n", delete=True)                    # listed, file missing
lit("unlisted.txt", "not in the manifest\n", listed=False)    # file exists, manifest has no row
(LIT / "MANIFEST.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8", newline="\n")

n = 0


def finding(name, evidence_lines=None, evidence=None):
    global n
    n += 1
    fm = [f'id: "FND-9{n:03d}"', "type: finding", "status: unverified-until-human-checks", "created_by: evidence-steward", 'created_utc: "2026-11-05"']
    fm.append("evidence: " + json.dumps(evidence or []))
    if evidence_lines is not None:
        fm.append("evidence_lines: " + json.dumps(evidence_lines))
    (WS / "findings" / f"SUM-9{n:03d}-{name}.md").write_text("---\n" + "\n".join(fm) + "\n---\n\n# fixture\n", encoding="utf-8", newline="\n")
    return f"SUM-9{n:03d}-{name}.md"


P = "evidence/literature-20261019/"
cases = [
    ("path form",                 finding("path", [P + "ok-a.txt"]), True),
    ("bare file name",            finding("bare", ["ok-b.txt"]), True),
    ("with a line range",         finding("range", [P + "ok-a.txt L1-5"]), True),
    ("manifest id has extension", finding("csv", ["raw-c.csv"]), True),
    ("two good files",            finding("two", [P + "ok-a.txt", "ok-b.txt"]), True),
    ("not in the manifest",       finding("unlisted", [P + "unlisted.txt"]), False),
    ("unknown file",              finding("ghost", ["ghost.txt"]), False),
    ("hash differs",              finding("tampered", [P + "tampered.txt"]), False),
    ("listed but missing",        finding("gone", [P + "gone.txt"]), False),
    ("good plus unknown",         finding("mixed", [P + "ok-a.txt", "ghost.txt"]), False),
    ("path traversal",            finding("travers", [P + "../../CLAUDE.md"]), False),
    ("outside path ignored",      finding("outside", ["design/package-v5/00-README.md"]), False),
    ("no citation at all",        finding("none"), False),
]

r = subprocess.run([sys.executable, "-I", "tools/verify_workspace.py"], capture_output=True, text=True, encoding="utf-8", cwd=WS)
out = r.stdout.splitlines()
bad = 0
for name, fn, want_ok in cases:
    mine = [l for l in out if fn in l and ("stored-literature" in l or "extract" in l or "EXT evidence" in l)]
    fails = [l for l in mine if l.startswith("FAIL")]
    passes = [l for l in mine if l.startswith("PASS")]
    ok = (bool(passes) and not fails) if want_ok else bool(fails)  # a rejected finding needs at least one FAIL; a PASS for its good file may sit beside it
    bad += not ok
    print(("PASS " if ok else "FAIL ") + f"{name}: expected {'accepted' if want_ok else 'rejected'}" + ("" if ok else f"   got {mine}"))

# the fixture literature must not leak into the real workspace
shutil.rmtree(root, ignore_errors=True)
print(f"failures {bad}")
sys.exit(1 if bad else 0)
