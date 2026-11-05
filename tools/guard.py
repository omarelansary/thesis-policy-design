#!/usr/bin/env python3
"""PreToolUse guard (deterministic). Configured in .claude/settings.json; fires for the lead and for every subagent.

Enforces, as far as a hook can:
  1. No direct tool access to the research repository, previous-thesis folders or earlier session transcripts, and no
     reads or writes outside the workspace (Read/Grep/Glob/Write/Edit path arguments; Bash/PowerShell command text).
     The sanctioned route to evidence is tools/origin_extract.py, which needs none of those names on its command line.
  2. Single-writer ownership: a named subagent may write only inside the globs listed for it in config/ownership.json.
  3. Immutable files: nobody may Write/Edit evidence/governing/**, evidence/sources.json, evidence/restricted.json,
     evidence/origin-index.tsv, config/origin.json, .git/**, .claude/settings.local.json via the file-edit tools.
  4. Agents may not edit configuration, instructions, tools or the authorization register. Recorded intake texts
     (requirements/intake/20*) may be created but, once they exist, not changed through the edit tools (CREATE_ONLY).
  5. SendMessage: recipients are limited to subagent ids (a + 16 hex) and "main"; and every message of a thread is
     counted in ops/threads/<thread>/messages.log against the cap in config/limits.json. With no active thread
     (ops/threads/ACTIVE.json written by the lead from a TASK.md) messaging is refused.
  6. git push (AUTH-020, AUTH-022): a command that runs git push is refused unless it is exactly `git push origin <branch>` or
     `git push -u origin <branch>` with <branch> = v5-audit or linux-from-v5-audit--portable-guard-and-short-state; force, delete,
     mirror, all, main and every other branch are refused. "Runs git push" is found on tokens, including through env, command, sudo,
     xargs, git's global options, aliases set with -c, bash -c / sh -c / python -c strings and heredocs fed to a shell.
Limits (see ops/SAFEGUARDS.md): Bash/PowerShell command text is matched by pattern, so an obfuscated command, an
interpreter one-liner or an unusual wildcard can still evade rule 1; rule 3 does not cover writes made through Bash;
whether a foreign agent id resolves to another session is untested. verify_workspace.py detects some tampering afterwards.
Exit code 2 blocks the call and returns the stderr message to the model. Other failures are fail-closed via onFailure=block.
"""
import datetime, json, os, pathlib, re, shlex, sys

WS = pathlib.Path(__file__).resolve().parents[1]
data = json.load(sys.stdin)
tool = data.get("tool_name", "")
ti = data.get("tool_input", {}) or {}
agent = data.get("agent_type")  # absent for the lead session

FORBIDDEN = re.compile(
    r"research-clean|cleanroom|thesis-back|claude_forensic|forensic_rescue|"
    r"[\\/]\.claude[\\/](projects|history|file-history|plans|backups|session-env)", re.I)
WIN = os.name == "nt"
# PARENT matches the workspace's parent directory and its siblings (anything under it except this workspace itself).
# Windows: drive letter in C:/ and MSYS /c/ forms. POSIX (AUTH-021): the absolute parent path; on Linux there is no drive letter,
# so the Windows form built from WS.parts[0] ('/') never matched and the rule failed open.
if WIN:
    _drive = WS.parts[0][0]
    PARENT = re.compile(
        r"(?:" + _drive + r":|/" + _drive + r")" + "".join(r"[\\/]+" + re.escape(p) for p in WS.parent.parts[1:])
        + r"(?![\\/]+" + re.escape(WS.name) + r"(?![\w.-]))", re.I)
elif len(WS.parent.parts) > 1:
    PARENT = re.compile(
        r"(?<![\w.-])" + "".join(r"/+" + re.escape(p) for p in WS.parent.parts[1:])
        + r"(?![\\/]+" + re.escape(WS.name) + r"(?![\w.-]))")
else:  # workspace directly under the filesystem root: no parent directory to protect
    PARENT = re.compile(r"(?!)")
DOTDOT = re.compile(r"(^|[\s\"'=(])\.\.(?=[\\/\s;&|)\"']|$)")
# Claude Code's per-session scratchpad: %LOCALAPPDATA%/Temp/claude/... on Windows, /tmp/claude-<uid>/... on Linux (AUTH-021)
SCRATCH = re.compile(r"[\\/]AppData[\\/]Local[\\/]Temp[\\/]claude[\\/]|^/tmp/claude-\d+/", re.I)
ALWAYS_IMMUTABLE = ["evidence/governing/**", "evidence/sources.json", "evidence/restricted.json", "evidence/origin-index.tsv",
                    "config/origin.json", ".git/**", ".claude/settings.local.json"]
CREATE_ONLY = ["requirements/intake/20*"]  # recorded intake texts: a new file may be created, an existing one may not be changed (edit tools only)
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
    m = re.match(r"^/([A-Za-z])/(.*)$", p) if WIN else None  # MSYS style /c/Users/... (Windows only: on Linux /c/... is a real path)
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
    static = re.split(r"[*?\[]", v.replace("\\", "/"), maxsplit=1)[0]  # the part before any wildcard must stay inside
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


# --- git push (AUTH-020, widened and hardened by AUTH-021/022) ---------------------------------------------------------------
# A command that runs `git push` is refused unless it is exactly one of the allowed forms. "Runs git push" is decided on tokens, not on
# a regex anchored at the start of the command, so `env git push`, `command git push`, `git -C x push`, `bash -c "git push ..."`,
# `git -c alias.p=push p` and a push inside a heredoc fed to a shell are all found, while `git commit -m "mention git push"`,
# `git log --grep push` and `grep "git push" file` are not pushes. Limits: variables (`$G push`), command substitution that builds the
# word `git`, a push configured in .git/config or a global git config, and scripts that build the command from fragments are not seen.
PUSH_OK = re.compile(r"\s*git push( -u)? origin (v5-audit|linux-from-v5-audit--portable-guard-and-short-state)\s*")
GIT_VALUE_OPTS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--super-prefix", "--config-env", "--attr-source"}
LOOSE_PUSH = re.compile(r"\bgit\b[^;&|\n]*\bpush\b", re.I)
RUNNERS = {"bash", "sh", "zsh", "dash", "ksh", "fish", "csh", "tcsh", "eval", "source", "pwsh", "powershell", "cmd", "python", "python3",
           "perl", "ruby", "node", "php", "lua", "ssh", "su", "watch", "parallel"}
RUNNER_WORD = re.compile(r"(?<![\w.-])(" + "|".join(sorted(RUNNERS)) + r")(?![\w-])", re.I)
HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")


def _tokens(text):
    try:
        lx = shlex.shlex(text.replace("`", " ; "), posix=True, punctuation_chars=True)
        lx.whitespace_split = True
        lx.commenters = ""
        return list(lx)
    except ValueError:  # unbalanced quotes
        return None


def _split_heredocs(cmd):
    """(command text without heredoc bodies, [(body, text before the <<)])"""
    lines, out, bodies, i = cmd.split("\n"), [], [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        for m in HEREDOC.finditer(line):
            body = []
            while i < len(lines) and lines[i].strip() != m.group(2):
                body.append(lines[i])
                i += 1
            i += 1
            bodies.append(("\n".join(body), line[:m.start()]))
    return "\n".join(out), bodies


def runs_git_push(cmd):
    text, bodies = _split_heredocs(cmd)
    for body, before in bodies:  # a heredoc fed to a shell or interpreter is a script
        if RUNNER_WORD.search(before) and LOOSE_PUSH.search(body):
            return True
    toks = _tokens(text)
    if toks is None:
        return bool(LOOSE_PUSH.search(text))
    scripts = any(t.replace("\\", "/").rsplit("/", 1)[-1].lower() in RUNNERS for t in toks)
    for i, t in enumerate(toks):
        if scripts and LOOSE_PUSH.search(t):  # bash -c "git push ...", python -c "...['git','push']..."
            return True
        if t.replace("\\", "/").rsplit("/", 1)[-1].lower() in ("git", "git.exe"):
            j = i + 1
            while j < len(toks) and toks[j].startswith("-"):
                a = toks[j]
                if (a == "-c" and j + 1 < len(toks) and toks[j + 1].lower().startswith("alias.")) or a.lower().startswith(("-calias.", "--config-env=alias.")):
                    return True  # an alias can be anything, including push
                j += 2 if a in GIT_VALUE_OPTS else 1
            if j < len(toks) and toks[j].lower() == "push":
                return True
    return False


def check_push(cmd):
    if runs_git_push(cmd) and not PUSH_OK.fullmatch(cmd):
        block("git push is allowed only as `git push origin v5-audit` or `git push -u origin v5-audit` (AUTH-020), or the same for the branch "
              "linux-from-v5-audit--portable-guard-and-short-state (AUTH-022), on its own.")


if tool == "SendMessage":
    thread_gate()
elif tool in ("Bash", "PowerShell"):
    check_text("this command", ti.get("command", ""))
    check_push(ti.get("command", ""))
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
    if match(r, CREATE_ONLY) and (WS / r).exists():
        block(f"{r} is a recorded intake text and already exists: corrections are new files, never edits (requirements/intake/README.md). Bash can still change it; verify_workspace.py detects that, it does not prevent it.")
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
