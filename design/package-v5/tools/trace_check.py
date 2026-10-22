"""Read-only traceability check for design/package-v5 and the V5 records (stdlib only).
Checks: every `L/<file>:<line>` or `L/<file>:<a>-<b>` pointer names an existing file in evidence/literature-20261019/
and lines inside its length; every EXT-/FND-/HYP-/DPR- id named exists as a record; every V5-Rnn and D-nn named in
04 appears in 06. Prints misses and exits 1 if any.
Run: python design/package-v5/tools/trace_check.py
"""
import pathlib, re, sys

WS = pathlib.Path(__file__).resolve().parents[3]
LIT = WS / "evidence" / "literature-20261019"
FILES = sorted((WS / "design" / "package-v5").glob("0*.md")) + [WS / "design/proposals" / f"DPR-000{i}.md" for i in (7, 8, 9)] \
    + [WS / "hypotheses" / f"HYP-00{i}.md" for i in range(15, 22)]
ids = set()
for d in ("evidence/extracts", "findings", "hypotheses", "design/proposals", "challenges", "reviews"):
    for p in (WS / d).glob("*.md"):
        m = re.search(r'^id:\s*"?([A-Z]+-\d+)"?', p.read_text(encoding="utf-8", errors="replace"), re.M)
        ids.add(m.group(1) if m else p.stem)
miss, n_ptr, n_id = [], 0, 0
lengths = {}
for f in FILES:
    if not f.exists():
        miss.append(f"missing file {f.relative_to(WS)}")
        continue
    t = f.read_text(encoding="utf-8")
    for m in re.finditer(r"L/([A-Za-z0-9._*-]+?\.(?:txt|md|py|dat|csv))((?:[:,]\s*:?\d+(?:-\d+)?)*)", t):
        name, lines = m.group(1), m.group(2)
        if "*" in name:
            continue
        n_ptr += 1
        p = LIT / name
        if not p.exists():
            miss.append(f"{f.name}: no file L/{name}")
            continue
        if name not in lengths:
            lengths[name] = p.read_text(encoding="utf-8", errors="replace").count("\n") + 1
        for a, b in re.findall(r"(\d+)(?:-(\d+))?", lines):
            if int(b or a) > lengths[name]:
                miss.append(f"{f.name}: L/{name}:{a}{'-' + b if b else ''} beyond {lengths[name]} lines")
    for r in set(re.findall(r"\b(EXT-\d{4}|FND-\d{4}|HYP-\d{4}|DPR-\d{4})\b", t)):
        n_id += 1
        if r not in ids:
            miss.append(f"{f.name}: unknown id {r}")
d04 = (WS / "design/package-v5/04-design.md").read_text(encoding="utf-8")
p06 = WS / "design/package-v5/06-contribution-and-traceability.md"
t06 = p06.read_text(encoding="utf-8") if p06.exists() else ""
for r in sorted(set(re.findall(r"\b(V5-R\d\d|D-\d\d)\b", d04))):
    if r not in t06:
        miss.append(f"06 lacks {r}")
print(f"pointers checked {n_ptr}, ids checked {n_id}, misses {len(miss)}")
for x in miss:
    print("MISS", x)
sys.exit(1 if miss else 0)
