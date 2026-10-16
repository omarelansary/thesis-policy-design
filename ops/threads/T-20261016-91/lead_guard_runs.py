"""Lead-run guard unit cases T1-T7 escalated by design-challenger (T-20261016-91). Feeds JSON to tools/guard.py only; executes nothing named in the JSON."""
import json, subprocess, sys
ws = r"C:\Users\omr\Documents\thesis-policy-design"
cases = [
 ("T1 Glob wildcard dir name", {"tool_name":"Glob","tool_input":{"pattern":"research-clean*/CLAUDE.md","path":"C:\\Users\\omr\\Documents"}}, 0),
 ("T2 Grep glob key", {"tool_name":"Grep","tool_input":{"pattern":"Stage","path":"C:\\Users\\omr\\Documents","glob":"research-cleanroom/**"}}, 0),
 ("T3 Bash ls wildcard", {"tool_name":"Bash","tool_input":{"command":"ls ../research-clean*"}}, 0),
 ("T4 Bash sanctioned-name comment", {"tool_name":"Bash","tool_input":{"command":"cat C:/Users/omr/Documents/research-cleanroom/CLAUDE.md # tools/verify_workspace.py"}}, 0),
 ("T5 proposer write .claude/settings.json", {"tool_name":"Write","tool_input":{"file_path":".claude/settings.json"},"agent_type":"design-proposer","cwd":ws}, 2),
 ("T6a lead write .git/config", {"tool_name":"Write","tool_input":{"file_path":".git/config"},"cwd":ws}, 0),
 ("T6b lead write .claude/settings.local.json", {"tool_name":"Write","tool_input":{"file_path":".claude/settings.local.json"},"cwd":ws}, 0),
 ("T7 SendMessage format-only id", {"tool_name":"SendMessage","tool_input":{"to":"a0000000000000000"}}, 0),
]
for n, d, exp in cases:
    r = subprocess.run([sys.executable, "tools/guard.py"], input=json.dumps(d), capture_output=True, text=True, cwd=ws)
    print(f"{n}: exit {r.returncode} (challenger expected {exp}) stderr={r.stderr.strip()!r}")
