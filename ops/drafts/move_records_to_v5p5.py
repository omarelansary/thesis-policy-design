"""Move the research-record commits of the Linux branch onto the current branch (v5-p5-break-even), the human's instruction of
2026-11-08 (INT-T-047): the Linux branch keeps only the Windows/Linux switch (up to 5abc9ac, AUTH-023).
For each commit in 5abc9ac..d2f65f5 (oldest first): cherry-pick without committing; set every file the commit touched to that
commit's exact version (so conflicts from the administrative STATE shortening resolve to the Linux branch's text); commit with the
original message, author and date. Prints the mapping old -> new. Runs only on v5-p5-break-even with a clean index.
"""
import subprocess, sys

def git(*a, check=True):
    r = subprocess.run(["git", *a], capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"git {' '.join(a)} failed: {r.stderr.strip()}")
    return r

if git("branch", "--show-current").stdout.strip() != "v5-p5-break-even":
    sys.exit("not on v5-p5-break-even")
if git("diff", "--cached", "--name-only").stdout.strip():
    sys.exit("index not clean")
commits = git("rev-list", "--reverse", "5abc9ac..d2f65f5").stdout.split()
for c in commits:
    git("cherry-pick", "--no-commit", c, check=False)
    files = git("diff-tree", "--no-commit-id", "--name-only", "-r", c).stdout.split()
    for f in files:
        exists = git("cat-file", "-e", f"{c}:{f}", check=False).returncode == 0
        if exists:
            git("checkout", c, "--", f)
            git("add", f)
        else:
            git("rm", "-q", "--cached", "--ignore-unmatch", f)
    unmerged = git("diff", "--name-only", "--diff-filter=U").stdout.strip()
    if unmerged:
        sys.exit(f"{c}: unresolved {unmerged}")
    git("commit", "-q", "-C", c)
    new = git("rev-parse", "--short", "HEAD").stdout.strip()
    print(c[:7], "->", new, git("log", "-1", "--format=%s", c).stdout.strip()[:70])
