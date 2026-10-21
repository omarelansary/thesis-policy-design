"""AUTH-020 step 0: the permission and tool changes of section J of ops/plans/v5-audit-plan-revised.md.
Written by the lead, to be REVIEWED AND RUN BY THE HUMAN (the auto-mode classifier refuses to let the lead change its own
permissions, guard or authorization record). Run from the workspace root on branch v5-audit:

    python ops/plans/step0-apply-AUTH-020.py --dry-run     (prints the diffs, writes nothing)
    python ops/plans/step0-apply-AUTH-020.py

Each edit checks that the file still holds the expected text and stops without writing anything if it does not.
Afterwards run, in this order:
    python ops/tests/guard_cases.py              (expect "failures 0")
    python tools/verify_workspace.py             (expect FAIL only for the pin mismatch of the four changed pinned files)
    python tools/verify_workspace.py --repin
    python tools/verify_workspace.py             (expect fail=0)
Then reload the VS Code window (or start a new Claude session) so the new permission rules load, and tell the lead to go.
"""
import json, pathlib, sys

R = pathlib.Path(__file__).resolve().parents[2]
staged = {}


def edit(rel, old, new, count=1):
    p = R / rel
    t = staged.get(rel, p.read_text(encoding="utf-8"))
    if t.count(old) != count:
        sys.exit(f"STOP: {rel} does not contain the expected text exactly {count} time(s); nothing was written.\n{old[:120]}")
    staged[rel] = t.replace(old, new)


# 1. .claude/settings.json: commit allowed; push only to v5-audit; branch checks, Agent and the V5 scripts allowed.
sp = R / ".claude/settings.json"
s = json.loads(sp.read_text(encoding="utf-8"))
perm = s["permissions"]
NEW_ALLOW = ["Bash(git commit*)", "Bash(git push origin v5-audit)", "Bash(git push -u origin v5-audit)",
             "Bash(git branch --show-current*)", "Bash(git rev-parse*)", "Agent",
             "Bash(python design/package-v5/calc/*)", "Bash(python design/package-v5/tools/*)",
             "Bash(python ops/tests/guard_cases.py*)", "Bash(python design/ledger/export_ledger.py*)"]
NEW_DENY = ["Bash(git push --force*)", "Bash(git push -f*)", "Bash(git push --all*)", "Bash(git push --mirror*)",
            "Bash(git push --delete*)", "Bash(git push *main*)"]
for need, lst in (("Bash(git commit*)", perm["ask"]), ("Bash(git push*)", perm["deny"])):
    if need not in lst:
        sys.exit(f"STOP: settings.json no longer has {need} where expected; nothing was written.")
if any(a in perm["allow"] for a in NEW_ALLOW):
    sys.exit("STOP: settings.json already has some AUTH-020 rules; nothing was written.")
perm["ask"].remove("Bash(git commit*)")
i = perm["deny"].index("Bash(git push*)")
perm["deny"][i:i + 1] = NEW_DENY  # PowerShell(git push*) stays denied
perm["allow"] += NEW_ALLOW
staged[".claude/settings.json"] = json.dumps(s, indent=2, ensure_ascii=False) + "\n"

# 2. tools/verify_workspace.py: the reviewed allow set gains the same rules (the deny check still finds "git push").
edit("tools/verify_workspace.py",
     '"WebSearch", "WebFetch"}  # WebSearch/WebFetch',
     '"WebSearch", "WebFetch", ' + ", ".join(json.dumps(a) for a in NEW_ALLOW)
     + '}  # AUTH-020 added commit, the v5-audit push, branch checks, Agent and the V5 scripts; WebSearch/WebFetch')

# 3. tools/guard.py: a push is refused unless it is exactly `git push [-u] origin v5-audit` (belt and braces).
edit("tools/guard.py",
     "Limits (see ops/SAFEGUARDS.md):",
     "  6. git push (AUTH-020): a command that runs git push is refused unless it is exactly `git push origin v5-audit`\n"
     "     or `git push -u origin v5-audit`; force, delete, mirror, all, main and every other branch are refused.\n"
     "Limits (see ops/SAFEGUARDS.md):")
edit("tools/guard.py",
     'if tool == "SendMessage":\n    thread_gate()',
     'PUSH = re.compile(r"(^|[;&|(]\\s*)git\\b[^;&|\\n]*\\bpush\\b")\n'
     'PUSH_OK = re.compile(r"\\s*git push( -u)? origin v5-audit\\s*")\n\n\n'
     'def check_push(cmd):\n'
     '    if PUSH.search(cmd) and not PUSH_OK.fullmatch(cmd):\n'
     '        block("git push is allowed only as `git push origin v5-audit` or `git push -u origin v5-audit`, on its own (AUTH-020).")\n\n\n'
     'if tool == "SendMessage":\n    thread_gate()')
edit("tools/guard.py",
     '    check_text("this command", ti.get("command", ""))',
     '    check_text("this command", ti.get("command", ""))\n    check_push(ti.get("command", ""))')

# 4. ops/tests/guard_cases.py: push cases.
edit("ops/tests/guard_cases.py",
     "# --- SendMessage and thread cap",
     "# --- git push (AUTH-020)\n"
     'case("push v5-audit", B("git push origin v5-audit"), 0)\n'
     'case("push -u v5-audit", B("git push -u origin v5-audit"), 0)\n'
     'case("push main", B("git push origin main"), 2)\n'
     'case("push v5-audit:main", B("git push origin v5-audit:main"), 2)\n'
     'case("push --force v5-audit", B("git push --force origin v5-audit"), 2)\n'
     'case("push other branch", B("git push origin other"), 2)\n'
     'case("push after cd &&", B("cd " + w.replace("\\\\", "/") + " && git push origin main"), 2)\n'
     'case("git -C push", B("git -C . push origin main"), 2)\n'
     'case("grep for the words git push is not a push", B(\'grep -n "git push" tools/guard.py\'), 0)\n'
     "# --- SendMessage and thread cap")

# 5. tools/litfetch.py: a fourth argument names the authorization, written to the manifest.
edit("tools/litfetch.py",
     "Usage: python tools/litfetch.py ID URL KIND        KIND = pdf | html | raw",
     "Usage: python tools/litfetch.py ID URL KIND AUTH   KIND = pdf | html | raw; AUTH = an id recorded in ops/AUTHORIZATIONS.md")
edit("tools/litfetch.py",
     "def main(sid, url, kind):\n",
     "def main(sid, url, kind, auth):\n"
     '    if not re.fullmatch(r"AUTH-\\d{3}", auth) or f"| {auth} |" not in open(os.path.join(WS, "ops", "AUTHORIZATIONS.md"), encoding="utf-8").read():\n'
     '        sys.exit("AUTH must be an authorization id recorded in ops/AUTHORIZATIONS.md")\n')
edit("tools/litfetch.py", '"auth": "AUTH-013"}', '"auth": auth}')
edit("tools/litfetch.py", "    if len(sys.argv) != 4:\n        sys.exit(__doc__)\n    main(*sys.argv[1:4])",
     "    if len(sys.argv) != 5:\n        sys.exit(__doc__)\n    main(*sys.argv[1:5])")

# 6. ops/AUTHORIZATIONS.md: the verbatim text of AUTH-020 (the table row is already in the working tree).
a = (R / "ops/AUTHORIZATIONS.md").read_text(encoding="utf-8")
if "| AUTH-020 |" not in a or "## AUTH-020 verbatim" in a:
    sys.exit("STOP: AUTHORIZATIONS.md lacks the AUTH-020 row or already has its verbatim section; nothing was written.")
staged["ops/AUTHORIZATIONS.md"] = a.rstrip("\n") + "\n" + r'''
## AUTH-020 verbatim human text (messages of 2026-10-22)
> look at this plan i created before i see the new work or chaanges to be added to the ledger, the idea of this plan as u can see is to be independent V5 audit critically thinking ans searching new opensource repos that beleived to solve sth or replace a componentn by a well established compeonet of work, or research or repos published by researchers.
>
> this was very general what i just said you will understand more and more from the plan, in the plan we should plan to also use multi agents like sonnet and stuff, but i want you to revesist it bec we added some parts from meeting notes and stuff, if you chaneged anything what did you change and why

> for number 2 what breifing?
> number 3 i wont provide june expose now, i ill leave it till we finish then we will test its ideas against what we found maybe we produce sth better than it, so we donot get contaminated now
>
> for the authrization i want you to checkout in a new branch, i will push the plans v5 md file plan and from there we can change all authrizations and what we want to complete V5 without being stopped or task fails bec of authorizations this is not an accepted failiure silent or was announced,

> goooo

Lead's interpretation (not the human's words): "change all authrizations ... to complete V5 without being stopped" is read as the permission changes in section J of the revised plan, limited to branch `v5-audit` and to the actions V5 needs; it does not lift the deny rules for the origin repository, previous-thesis folders, transcripts, installs, remotes, pulls, clones or git configuration, nor the guard's ownership and workspace rules. "goooo" is the start signal for step 0. Pushes by the lead to `v5-audit` are an exception to CLAUDE.md line 11 and AUTH-012 for that branch only. The human pushed f0b9ae5 to `origin/v5-audit` before the start signal. The auto-mode classifier refused the lead's own edits to permissions, the guard and this register as self-modification, so the human applied them with `ops/plans/step0-apply-AUTH-020.py`.
'''

if "--dry-run" in sys.argv:  # print the diffs, write nothing
    import difflib
    for rel, text in staged.items():
        old = (R / rel).read_text(encoding="utf-8").splitlines(keepends=True)
        sys.stdout.writelines(difflib.unified_diff(old, text.splitlines(keepends=True), "a/" + rel, "b/" + rel, n=1))
    sys.exit("dry run: nothing written")
for rel, text in staged.items():
    (R / rel).write_text(text, encoding="utf-8", newline="\n")
    print("written", rel)
print("done; now run the four commands in the docstring")
