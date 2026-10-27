"""Record the result of the literature verification (design/package-v5/13, RV-0024) in the ledger, in place: N-40 to PARTLY ANSWERED
(done, with the open computation named), N-39 updated (official ranges, corrected handling note). Appends Change log rows above the
append-only note. Refuses to run twice. Run from the repository root, then run design/ledger/export_ledger.py.
"""
import re, sys
from openpyxl import load_workbook

SRC = "design/ledger/PROJECT_A_OPEN_ITEMS_LEDGER.xlsx"
D, BY = "2026-10-27", "Claude"
wb = load_workbook(SRC)
L, C = wb["Ledger"], wb["Change log"]
lh = [c.value for c in L[1]]
rows = {L.cell(r, 1).value: r for r in range(2, L.max_row + 1) if L.cell(r, 1).value}
col = lambda n: lh.index(n) + 1
if "literature verification done" in str(L.cell(rows["N-40"], col("What is known now")).value):
    sys.exit("already applied; nothing written")
log = []


def note(lid, field, old, new, reason):
    log.append([D, lid, field, old, new, reason, "INT-T-012 / V5", BY])


def setf(lid, field, new, reason):
    r = rows[lid]; c = col(field); old = L.cell(r, c).value; L.cell(r, c).value = new; note(lid, field, old, new, reason)


def known(lid, text):
    r = rows[lid]; c = col("What is known now"); old = L.cell(r, c).value or ""
    L.cell(r, c).value = (old + " | " if old else "") + f"V5 {D}: " + text
    note(lid, "What is known now", "(appended)", text[:180], "design/package-v5/13")


known("N-40", "literature verification done (scouts T-118, stewards FND-0043..0045, challenger RV-0024 with CH-0105..0114, all accepted and applied): the equation structure is printed in 2607.12161, 2604.22750 and 2608.01347 (one write class; W1, S, X and T have no printed equation); 7:2:1 is an assumed weighting (output share measured at 0.5-1% of tokens, not 10%); official price pages give r 0.02-0.50 (several hosts list no cache price), w 1.0 (1.25 only Alibaba explicit), o 2.1-7.5; no published break-even for client-side tool discovery or memory seeding found in the stored set; the lead's seed arithmetic missed a core-prefix re-read (fixed). Details: design/package-v5/13")
setf("N-40", "Current status", "PARTLY ANSWERED", "13 written; two items remain")
setf("N-40", "Next action", "Optional, arithmetic only: add an uncached-core and a cold-cache column to D-04 (CH-0111); store the scouts' queries if the human wants the absence claims auditable (CH-0112)", "design/package-v5/13 s7")
setf("N-40", "Status date", D, "RV-0024 applied")
setf("N-40", "Status basis (evidence pointer)", "design/package-v5/13-literature-verification.md; findings/SUM-0045..0047; reviews/RV-0024.md", "RV-0024 applied")
known("N-39", "revised with official pages (11 rev 2): r 0.02-0.50 over the pages stored (some hosts list no cache price), w 1.0 (1.25 only Alibaba explicit), o 2.1-7.5, seven reference cases; D-04 grid extended to r 0.02 and restated: price matters at T = 3 and for one-match long sessions, and model independence is not shown. The handling proposal (token classes plus r, w, o; dollars under one or two cases) is unchanged and still the human's to accept")

note_row = next(i for i in range(C.max_row, 1, -1) if str(C.cell(i, 1).value or "").startswith("Append-only"))
C.insert_rows(note_row - 1, amount=len(log))
for i, row in enumerate(log):
    for j, v in enumerate(row):
        C.cell(note_row - 1 + i, j + 1).value = v
bad = [i for i in range(2, L.max_row + 1) if L.cell(i, 1).value and any(not (isinstance(L.cell(i, c).value, str) and re.search(rf"{ref}{i}\b", L.cell(i, c).value)) for c, ref in ((4, "C"), (5, "A")))]
assert not bad, f"formula check failed at rows {bad[:5]}"
wb.save(SRC)
print("change-log rows", len(log))
