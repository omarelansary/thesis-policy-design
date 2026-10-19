# design/ledger/: the Project A open-items ledger

**Canonical copy:** `PROJECT_A_OPEN_ITEMS_LEDGER.xlsx` (one row per open item, stable IDs, a Questions sheet for answers, Archive for closed rows, an append-only Change log). Status: tracked working document, record class SUM (unverified); authority for the work on it: `ops/AUTHORIZATIONS.md` AUTH-016.

**Derived copy:** `export/*.csv`, written by `python design/ledger/export_ledger.py` (read-only; formula columns computed by the script). The CSVs exist so that a commit's diff shows which items changed. Never edit them by hand; regenerate them in the same commit as any workbook change.

## Rules (also in the workbook README and Rules sheet)
- Edit the workbook in place. Never rebuild it from a script: that would overwrite typed answers.
- One row per item, ever. IDs are never reused or renumbered; merged items get status `SUPERSEDED / MERGED` and a pointer. Other names (SRC-06/07 rows, CH-, HYP-, REQ-, REGISTER Q) live in the Aliases sheet.
- A closure needs a basis (EXT id, file and lines, stored source id). Closing a decision item needs the decision-maker's own words and date, recorded verbatim.
- Repo evidence first; if the repo has none, public web search/fetch for that named item, stored with URL, time and SHA-256 (AUTH-016). No experiments, no implementation, no choice of thesis question, policy or parameters.
- Closed rows move from `Ledger` to `Archive` in the same commit; every status change gets a Change log row.
- Overview checks (duplicates, orphan links) must read 0 after recalculation in a spreadsheet program (Excel, LibreOffice or Google Sheets); `export_ledger.py` does not need recalculation.
- Each batch of closures is one local commit that names the ledger IDs and AUTH-016. The human pushes.

Joaa's statements are recorded verbatim (sheet "Supervisor statements") and treated as his proposals, not as established findings or requirements, until he confirms.
