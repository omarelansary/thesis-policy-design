#!/usr/bin/env python3
"""PreToolUse guard (deterministic). Configured in .claude/settings.json; fires for the lead and for every subagent.

Enforces, as far as a hook can:
  1. No direct tool access to the research repository, previous-thesis folders or earlier session transcripts, and no
     reads or writes outside the workspace (Read/Grep/Glob/Write/Edit path arguments; Bash/PowerShell command text).
     The sanctioned route to evidence is tools/origin_extract.py, which needs none of those names on its command line.
  2. Single-writer ownership: a named subagent may write only inside the globs listed for it in config/ownership.json.
  3. Immutable files: nobody may Write/Edit evidence/governing/**, evidence/sources.json, evidence/restricted.json,
     evidence/origin-index.tsv, config/origin.json, .git/**, .claude/settings.local.json via the file-edit tools.
  4. Agents may not edit configuration, instructions, tools or the authorization register.
  5. SendMessage: recipients are limited to subagent ids (a + 16 hex) and "main"; and every message of a thread is
     counted in ops/threads/<thread>/messages.log against the cap in config/limits.json. With no active thread
     (ops/threads/ACTIVE.json written by the lead from a TASK.md) messaging is refused.
Limits (see ops/SAFEGUARDS.md): Bash/PowerShell command text is matched by pattern, so an obfuscated command, an
interpreter one-liner or an unusual wildcard can still evade rule 1; rule 3 does not cover writes made through Bash;
whether a foreign agent id resolves to another session is untested. verify_workspace.py detects some tampering afterwards.
Exit code 2 blocks the call and returns the stderr message to the model. Other failures are fail-closed via onFailure=block.
"""
import datetime, json, os, pathlib, re, sys

WS = pathlib.Path(__file__).resolve().parents[1]
data = json.load(sys.stdin)
tool = data.get("tool_name", "")
ti = data.get("tool_input", {}) or {}
agent = data.get("agent_type")  # absent for the lead session

FORBIDDEN = re.compile(
    r"research-clean|cleanroom|thesis-back|claude_forensic|forensic_rescue|"
    r"[\\/]\.claude[\\/](projects|history|file-history|plans|backups|session-env)", re.I)
_drive = WS.parts[0][0]
PARENT = re.compile(
    r"(?:" + _drive + r":|/" + _drive + r")" + "".join(r"[\\/]+" + re.escape(p) for p in WS.parent.parts[1:])
    + r"(?![\\/]+" + re.escape(WS.name) + r"(?![\w.-]))", re.I)
DOTDOT = re.compile(r"(^|[\s\"'=(])\.\.(?=[\\/\s;&|)\"']|$)")
SCRATCH = re.compile(r"[\\/]AppData[\\/]Local[\\/]Temp[\\/]claude[\\/]", re.I)
ALWAYS_IMMUTABLE = ["evidence/governing/**", "evidence/sources.json", "evidence/restricted.json", "evidence/origin-index.tsv",
                    "config/origin.json", ".git/**", ".claude/settings.local.json"]
AGENT_FORBIDDEN_WRITE = [".claude/**", "CLAUDE.md", "tools/**", "config/**", "ops/AUTHORIZATIONS.md", "ops/STATE.md",
                         "ops/threads/ACTIVE.json", "ops/threads/*/messages.log", ".gitignore", ".gitattributes"]


def block(msg):
    print("BLOCKED by tools/guard.py: " + msg, file=sys.stderr)
    sys.exit(2)


def is_abs(p):
    return bool(re.match(r"^[A-Za-z]:/|^/", p))


def norm(p, cwd=None):
    """Absolute, normalised, forward-slash path ('..' and '.' resolved)."""
    p = str(p).replace("\\", "/")
    m = re.match(r"^/([A-Za-z])/(.*)$", p)  # MSYS style /c/Users/...
    if m:
        p = m.group(1) + ":/" + m.group(2)
    if not is_abs(p):
        p = str(cwd or data.get("cwd") or WS).replace("\\", "/") + "/" + p
    return os.path.normpath(p).replace("\\", "/")


def rel(p):
    """Workspace-relative path, or the absolute path when outside the workspace."""
    n = norm(p)
    ws = str(WS).replace("\\", "/")
    if n.lower() == ws.lower():
        return "."
    if n.lower().startswith(ws.lower() + "/"):
        return n[len(ws) + 1:]
    return n


def outside(r):
    return is_abs(r)


def glob_re(g):
    out, i = "", 0
    while i < len(g):
        if g.startswith("**", i):
            out += ".*"
            i += 2
        elif g[i] == "*":
            out += "[^/]*"
            i += 1
        else:
            out += re.escape(g[i])
            i += 1
    return out


def match(path, globs):
    return any(re.fullmatch(glob_re(g), path) for g in globs)


def check_text(label, text):
    if re.search(r"settings[.]local", text, re.I):
        block(f"{label} touches settings.local: a local settings file can switch every hook off (disableAllHooks). Ask the human.")
    if FORBIDDEN.search(text):
        block(f"{label} names the research repository, previous-thesis folders or earlier transcripts. "
              "Use `python tools/origin_extract.py` for evidence; ask the human to authorize anything else.")
    if PARENT.search(text) or DOTDOT.search(text):
        block(f"{label} refers to a location outside the workspace (parent directory or '..'). "
              "Agents work inside the workspace only; ask the human.")


def check_read_path(label, v):
    if FORBIDDEN.search(v):
        block(f"direct access to '{v}' is not allowed. Use `python tools/origin_extract.py`.")
    if DOTDOT.search(v):
        block(f"{label} '{v}' uses '..'. Stay inside the workspace.")
    static = re.split(r"[*?\[]", v.replace("\\", "/"), 1)[0]  # the part before any wildcard must stay inside
    if static:
        r = rel(static.rstrip("/") or ".")
        if outside(r) and not SCRATCH.search(r):
            block(f"{label} '{v}' resolves outside the workspace. Read only inside the workspace; ask the human otherwise.")


def thread_gate():
    to = str(ti.get("to", ""))
    if not (re.fullmatch(r"a[0-9a-f]{16}", to) or to == "main"):
        block(f"SendMessage recipient '{to}' is not allowed: use a subagent id or 'main'. Messages to other sessions need a human.")
    act = WS / "ops" / "threads" / "ACTIVE.json"
    if not act.exists():
        block("no active thread: the lead must write ops/threads/ACTIVE.json from a TASK.md (ops/PROTOCOL.md) before any message is sent.")
    a = json.loads(act.read_text(encoding="utf-8"))
    lim = json.loads((WS / "config" / "limits.json").read_text(encoding="utf-8"))
    cap = min(int(a["cap"]), int(lim["thread_message_cap"]))
    thread = a["thread"]
    if not re.fullmatch(r"T-\d{8}-\d{2}", thread):
        block("ops/threads/ACTIVE.json has an invalid thread id.")
    d = WS / "ops" / "threads" / thread
    if not d.is_dir():
        block(f"thread directory {d.name} does not exist.")
    log = d / "messages.log"
    n = len(log.read_text(encoding="utf-8").splitlines()) if log.exists() else 0
    if n >= cap:
        block(f"thread {thread} has reached its message cap ({n}/{cap}). Send nothing more: finish with your final answer, "
              "listing unresolved disagreements verbatim. Only the human may raise the cap.")
    with open(log, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"{datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}\t{agent or 'lead'}\t->\t{to}\t{n + 1}/{cap}\n")


if tool == "SendMessage":
    thread_gate()
elif tool in ("Bash", "PowerShell"):
    check_text("this command", ti.get("command", ""))
elif tool in ("Read", "Grep", "Glob"):
    for k in ("file_path", "path"):
        v = ti.get(k)
        if isinstance(v, str) and v:
            check_read_path(k, v)
    for k in ("pattern", "glob"):
        v = ti.get(k)
        if isinstance(v, str) and v:
            if FORBIDDEN.search(v):
                block(f"{k} '{v}' names a forbidden location. Use `python tools/origin_extract.py`.")
            if DOTDOT.search(v) or (tool == "Glob" and k == "pattern" and is_abs(v.replace("\\", "/"))):
                check_read_path(k, v)
elif tool in ("Write", "Edit", "NotebookEdit", "MultiEdit"):
    p = ti.get("file_path") or ti.get("notebook_path") or ""
    r = rel(p)
    if FORBIDDEN.search(str(p)) or FORBIDDEN.search(r):
        block("writing to the research repository or session stores is not allowed.")
    if outside(r) and not SCRATCH.search(r):
        block(f"writes outside the workspace are not allowed: {p}")
    if match(r, ALWAYS_IMMUTABLE):
        block(f"{r} is protected (immutable evidence, git internals or local settings override); changes need a human-authorized step.")
    if agent:
        own = json.loads((WS / "config" / "ownership.json").read_text(encoding="utf-8"))
        if match(r, AGENT_FORBIDDEN_WRITE):
            block(f"agent '{agent}' may not edit {r} (configuration, instructions, tools, thread control files and the authorization register belong to the lead and the human).")
        allowed = own.get("agents", {}).get(agent)
        if allowed is None:
            block(f"agent type '{agent}' has no write ownership entry in config/ownership.json; write nothing.")
        if not match(r, allowed):
            block(f"single-writer rule: agent '{agent}' may write only {allowed}; {r} belongs to another owner. "
                  "Send the content to its owner with SendMessage instead.")
sys.exit(0)
