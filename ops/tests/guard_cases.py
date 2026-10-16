"""Deterministic table of guard cases. Runs tools/guard.py from a THROWAWAY copy of the workspace skeleton
(tools/ + config/ + a fake thread), so message counting never touches real thread state.
Run: python ops/tests/guard_cases.py     (exit 1 if any case fails)"""
import json, os, pathlib, shutil, subprocess, sys, tempfile

SRC = pathlib.Path(__file__).resolve().parents[2]
TMP = pathlib.Path(tempfile.mkdtemp(prefix="tpd-guardtest-"))
WS = TMP / "thesis-policy-design"
(WS / "tools").mkdir(parents=True)
shutil.copy(SRC / "tools" / "guard.py", WS / "tools" / "guard.py")
shutil.copytree(SRC / "config", WS / "config")
(WS / "ops" / "threads" / "T-20260101-01").mkdir(parents=True)
w = str(WS)
ID = "a18792284f77dc047"


def run(d):
    r = subprocess.run([sys.executable, str(WS / "tools" / "guard.py")], input=json.dumps(d), capture_output=True, text=True, cwd=w)
    return r.returncode, r.stderr.strip()


def case(name, d, exp):
    global bad
    code, err = run(d)
    ok = code == exp
    bad += not ok
    print(("PASS " if ok else "FAIL ") + name + f"  exit={code} expected={exp}" + ("" if ok else "  " + err[:200]))


bad = 0
W = lambda path, agent=None, **k: {"tool_name": "Write", "tool_input": {"file_path": path}, "cwd": w, **({"agent_type": agent} if agent else {}), **k}
B = lambda cmd: {"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": w}
# --- lead writes
case("lead write inside (abs)", W(w + r"\findings\x.md"), 0)
case("lead write inside (rel)", W("findings/x.md"), 0)
case("lead write outside (abs)", W(r"C:\Users\omr\Documents\other\x.md"), 2)
case("lead write ../ escape", W("../x.md"), 2)
case("lead write origin", W(r"C:\Users\omr\Documents\research-cleanroom\a.md"), 2)
case("lead write immutable sources.json", W(w + r"\evidence\sources.json"), 2)
case("lead write immutable via traversal", W("design/../evidence/governing/INDEX.json"), 2)
case("lead write .git/config (T6a)", W(".git/config"), 2)
case("lead write settings.local.json (T6b)", W(".claude/settings.local.json"), 2)
case("lead write settings.json (allowed, human-visible in git)", W(".claude/settings.json"), 0)
# --- agent writes
case("steward own area", W(w + r"\findings\FND-1.md", "evidence-steward"), 0)
case("proposer into steward area", W(w + r"\findings\FND-1.md", "design-proposer"), 2)
case("steward traversal to tools", W("findings/../tools/guard.py", "evidence-steward"), 2)
case("steward abs traversal to config", W(w + r"\findings\..\config\ownership.json", "evidence-steward"), 2)
case("proposer write .claude/settings.json (T5)", W(".claude/settings.json", "design-proposer"), 2)
case("proposer write ops/threads/ACTIVE.json", W("ops/threads/ACTIVE.json", "design-proposer"), 2)
case("proposer write messages.log", W("ops/threads/T-20260101-01/messages.log", "design-proposer"), 2)
case("proposer own thread file", W("ops/threads/T-20260101-01/design-proposer.md", "design-proposer"), 0)
case("proposer other agent's thread file", W("ops/threads/T-20260101-01/design-challenger.md", "design-proposer"), 2)
case("unknown agent type (Explore)", W("findings/a.md", "Explore"), 2)
# --- reads
case("Read inside workspace", {"tool_name": "Read", "tool_input": {"file_path": w + r"\CLAUDE.md"}, "cwd": w}, 0)
case("Read origin path", {"tool_name": "Read", "tool_input": {"file_path": r"C:\Users\omr\Documents\research-cleanroom\CLAUDE.md"}, "cwd": w}, 2)
case("Read outside workspace", {"tool_name": "Read", "tool_input": {"file_path": r"C:\Users\omr\Documents\notes.txt"}, "cwd": w}, 2)
case("Read ../ relative", {"tool_name": "Read", "tool_input": {"file_path": "../x.md"}, "cwd": w}, 2)
case("Glob wildcard dir + parent path (T1)", {"tool_name": "Glob", "tool_input": {"pattern": "research-clean*/CLAUDE.md", "path": r"C:\Users\omr\Documents"}, "cwd": w}, 2)
case("Glob absolute parent pattern", {"tool_name": "Glob", "tool_input": {"pattern": "C:/Users/omr/Documents/*/CLAUDE.md"}, "cwd": w}, 2)
case("Glob inside workspace", {"tool_name": "Glob", "tool_input": {"pattern": "evidence/**/*.md"}, "cwd": w}, 0)
case("Grep parent dir + glob key (T2)", {"tool_name": "Grep", "tool_input": {"pattern": "Stage", "path": r"C:\Users\omr\Documents", "glob": "research-cleanroom/**"}, "cwd": w}, 2)
case("Grep inside workspace", {"tool_name": "Grep", "tool_input": {"pattern": "Stage", "path": "evidence"}, "cwd": w}, 0)
case("Grep glob with ..", {"tool_name": "Grep", "tool_input": {"pattern": "x", "glob": "../*/CLAUDE.md"}, "cwd": w}, 2)
# --- shell text
case("Bash ls ../research-clean* (T3)", B("ls ../research-clean*"), 2)
case("Bash cd ..", B("cd .. && ls"), 2)
case("Bash parent dir ls (msys form)", B("ls /" + str(TMP).replace("\\", "/").replace(":", "", 1).lstrip("/")), 2)
case("Bash parent dir ls (windows form)", B("dir " + str(TMP)), 2)
case("Bash origin + sanctioned-name comment (T4)", B("cat C:/Users/omr/Documents/research-cleanroom/CLAUDE.md # tools/verify_workspace.py"), 2)
case("Bash sanctioned tool", B("python tools/origin_extract.py --list-sources"), 0)
case("Bash verify", B("python tools/verify_workspace.py --quick"), 0)
case("Bash own absolute path", B("cd " + w.replace("\\", "/") + " && git status"), 0)
case("Bash 'git log' file with dots in name", B("git log --oneline -- a..b"), 0)
case("PowerShell origin", {"tool_name": "PowerShell", "tool_input": {"command": r"Get-Content C:\Users\omr\Documents\research-cleanroom\CLAUDE.md"}, "cwd": w}, 2)
case("Bash writes settings.local.json", B("echo {} > .claude/settings.local.json"), 2)
case("PowerShell writes settings.local.json", {"tool_name": "PowerShell", "tool_input": {"command": "Set-Content .claude/settings.local.json x"}, "cwd": w}, 2)
# --- SendMessage and thread cap
M = lambda to, **k: {"tool_name": "SendMessage", "tool_input": {"to": to}, **k}
case("msg with no active thread", M(ID), 2)
(WS / "ops" / "threads" / "ACTIVE.json").write_text(json.dumps({"thread": "T-20260101-01", "cap": 3}))
case("msg to peer session name", M("research-cleanroom-21"), 2)
case("msg to peer session ref", M("3ee433"), 2)
case("msg to arbitrary name", M("ping"), 2)
case("msg 1 of 3 (agent id)", M(ID), 0)
case("msg 2 of 3 (main, from agent)", M("main", agent_type="design-proposer"), 0)
case("msg 3 of 3", M(ID), 0)
case("msg 4 over cap", M(ID), 2)
case("msg 5 over cap (to main also blocked)", M("main"), 2)
(WS / "ops" / "threads" / "ACTIVE.json").write_text(json.dumps({"thread": "T-20260101-01", "cap": 99}))
case("ACTIVE cap above limits.json is clamped (log already 3, limit 12 -> allowed until 12)", M(ID), 0)
n = len((WS / "ops" / "threads" / "T-20260101-01" / "messages.log").read_text().splitlines())
print(f"INFO messages.log lines: {n}")
for i in range(20):
    run(M(ID))
n2 = len((WS / "ops" / "threads" / "T-20260101-01" / "messages.log").read_text().splitlines())
bad += n2 != 12
print(("PASS " if n2 == 12 else "FAIL ") + f"hard cap from config/limits.json stops at 12 (log has {n2})")
shutil.rmtree(TMP, ignore_errors=True)
print(f"failures {bad}")
sys.exit(1 if bad else 0)
