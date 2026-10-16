# Record types, ids and rules

Front matter is `key: value` lines between `---` markers (values may be JSON). `tools/verify_workspace.py` checks the rules marked (V).

| Type | Id | Directory | Writer | Required front matter | Rules |
|---|---|---|---|---|---|
| extract | EXT-NNNN | evidence/extracts/ | tools/origin_extract.py | set by the tool | verbatim body re-checked against the source (V) |
| finding | FND-NNNN | findings/ | evidence-steward | id, type, status, created_by, created_utc, evidence[] | cites at least one EXT (V); status proposed / accepted (accepted needs human + AUTH) |
| hypothesis | HYP-NNNN | hypotheses/ | design-proposer | + basis[], falsifier | falsifier non-empty (V) |
| design proposal | DPR-NNNN | design/proposals/ | design-proposer | + basis[] | draft for challenge; never a decision |
| design choice | DES-NNNN | design/choices/ | design-proposer drafts, human approves | + basis[], alternatives[], falsifier | `approved` requires `approved_by: human` and `authorization: AUTH-nnn` that exists (V) |
| challenge | CH-NNNN | challenges/ | design-challenger | + target, severity | status open / answered / resolved / escalated / withdrawn |
| review | RV-NNNN | reviews/ | design-challenger | + target | |
| requirement | REQ-xx | requirements/REGISTER.md | lead | row in the register | text lives in an EXT; ids must resolve (V) |
| summary | SUM-NNNN | any (own directory of the writer) | any | type: summary, derived_from[] | unverified until checked against EXT |
| thread | T-YYYYMMDD-NN | ops/threads/ | lead (TASK.md, SUMMARY.md); each agent writes its own `<agent>.md` | | see ops/PROTOCOL.md |
| authorization | AUTH-nnn | ops/AUTHORIZATIONS.md | lead records, human grants | date, verbatim human quote | an agent can never create one (V checks quote present) |
| workspace decision | WD-nnn | ops/DESIGN-DECISIONS.md | lead | | decisions about how the workspace works, not about the thesis |

## Statement labels
[F] fact stated in a cited source (with EXT id) · [O] observation made by running something · [I] interpretation · [U] unknown · [S] speculation. A "finding" is a claim about what sources say or what was observed; it is not a scientific conclusion until the human accepts it.

## Ids
Allocated sequentially by the writer (check the directory for the next free number; the extract tool reserves its ids atomically). Ids are never reused. Superseding a record = new record with `supersedes: ID`; the old one stays.
