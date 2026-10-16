"""C3: tamper detection. For each case, copies the workspace to a throwaway directory, applies ONE tamper, runs
`python tools/verify_workspace.py --quick` there and checks that the expected FAIL line appears.
Run: python ops/tests/c3_tamper.py   (exit 1 if a case is not detected, or if the untampered copy fails)"""
import json, pathlib, re, shutil, subprocess, sys, tempfile

SRC = pathlib.Path(__file__).resolve().parents[2]
bad = 0


def fresh():
    d = pathlib.Path(tempfile.mkdtemp(prefix="tpd-c3-")) / "thesis-policy-design"
    shutil.copytree(SRC, d, ignore=shutil.ignore_patterns(".git", "raw", "__pycache__"))
    return d


def verify(d):
    r = subprocess.run([sys.executable, "tools/verify_workspace.py", "--quick"], capture_output=True, text=True, encoding="utf-8", cwd=d)
    return r.returncode, r.stdout


def edit(d, rel, fn):
    p = d / rel
    p.write_bytes(fn(p.read_bytes().decode("utf-8")).encode("utf-8"))


def run(name, tamper, expect):
    global bad
    d = fresh()
    try:
        tamper(d)
        code, out = verify(d)
        fails = [l for l in out.splitlines() if l.startswith("FAIL")]
        if expect is None:
            ok = code == 0 and not fails
        else:
            ok = code != 0 and any(re.search(expect, l) for l in fails)
        bad += not ok
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"   expected /{expect}/, got: {fails[:3]}"))
    finally:
        shutil.rmtree(d.parent, ignore_errors=True)


run("baseline copy verifies clean", lambda d: None, None)
run("modified governing copy", lambda d: (d / "evidence/governing/decisions/D13-audit-closure-and-return-to-selection.md").open("a").write("x"), r"governing copy MODIFIED")
run("altered extract body", lambda d: edit(d, "evidence/extracts/EXT-0001.md", lambda t: t.replace("Research target", "Research targets", 1)), r"EXT-0001.*DIFFERS")


def withheld(d):
    h = __import__("hashlib").sha256((d / "templates/review.md").read_bytes()).hexdigest()
    r = json.loads((d / "evidence/restricted.json").read_text(encoding="utf-8"))
    r["withheld"][next(iter(r["withheld"]))]["sha256"] = h
    (d / "evidence/restricted.json").write_text(json.dumps(r), encoding="utf-8")


run("copy of a withheld file appears (synthetic)", withheld, r"WITHHELD FILE COPIED")
run("agent model changed", lambda d: edit(d, ".claude/agents/design-proposer.md", lambda t: t.replace("model: claude-sonnet-5-5", "model: opus", 1)), r"design-proposer: model is opus")


def remote(d):
    subprocess.run(["git", "init", "-q", str(d)], check=True)
    subprocess.run(["git", "-C", str(d), "remote", "add", "x", "https://example.invalid/x.git"], check=True)


run("git remote added", remote, r"git remote present")
run("settings.local.json override present", lambda d: (d / ".claude/settings.local.json").write_text("{}"), r"settings\.local\.json exists")
run("guard.py silently weakened", lambda d: edit(d, "tools/guard.py", lambda t: t + "\n# weakened\n"), r"differs from config/PINNED")
run("allow list widened", lambda d: edit(d, ".claude/settings.json", lambda t: t.replace('"Bash(git add *)"', '"Bash(git add *)", "Bash(curl *)"', 1)), r"allow list differs")
run("hook matcher drops SendMessage", lambda d: edit(d, ".claude/settings.json", lambda t: t.replace("|SendMessage", "", 1)), r"does NOT cover SendMessage")
run("limits.json cap raised", lambda d: edit(d, "config/limits.json", lambda t: t.replace('"thread_message_cap": 12', '"thread_message_cap": 99', 1)), r"differs from config/PINNED")


def approved(d):
    t = (d / "templates/design-choice.md").read_text(encoding="utf-8")
    t = t.replace("status: proposed", "status: approved", 1) if "status: proposed" in t else t.replace("status: draft", "status: approved", 1)
    t = t.replace("id: DES-0000", "id: DES-9001", 1)
    t = re.sub(r"^---\n", "---\napproved_by: human\nauthorization: AUTH-001\n", t, 1)
    (d / "design/choices/DES-9001.md").write_text(t, encoding="utf-8")


run("record 'approved' citing AUTH-001", approved, r"design-level AUTH")
print(f"failures {bad}")
sys.exit(1 if bad else 0)
