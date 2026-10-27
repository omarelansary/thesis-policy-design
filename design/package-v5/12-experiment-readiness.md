# 12. Experiment readiness: what can start, what cannot, and what the authorization would need to say

Status: provisional, lead, 2026-10-27. This is an assessment and a draft scope, not an authorization: no experiment, harness code or API call by the lead is authorized by it (AUTH-020 limits; REQ-U22-16 says the human will extend AUTH-020 when told the lead is ready). The loop rule of `05` stands: small items, read the result, revise, then the next item (REQ-U21-06).

## 1. Readiness by loop item
| Item (`05`) | Question | Ready? | What exists | What is missing |
|---|---|---|---|---|
| P0 part 4 | Is the cache a plain prefix cache? How long does it live? | **Yes** | `tools/p0_api_probe_v3.py`, human-run | The human's run (about 8 requests per model, plus a one-request lifetime mode to repeat later) |
| **P5** | Where is the regime break-even on this route, and are deferred definitions billed? | **Yes, once authorized** | D-01 and D-04 (the arithmetic and its price range), the API's usage fields, a stub-tool pattern from the probes | A harness (new code, written by the lead, run by the human): stub catalogues of several sizes, two arms (all tools in the prefix; a small core plus definitions appended after a scripted search), a fixed session length, usage recorded per request. About 80 requests per model, no accuracy measured |
| P3 | Do models search for a deferred tool without being told to? | **Not yet** | The recovery design (`04`), the absent-tool probe (one run per model) | A task set with a ground-truth tool per task, a catalogue with natural descriptions, a client-side search tool, the cells and prompt variants of `05` (desk work, no key; then about 160 requests per model) |
| P1 | Does memory-informed offering help returning users? | **No** | HYP-0017, D-02 (the threshold) | A multi-session vehicle or a thin generator of user histories (none found, `03` section 9), the memory file format, a task set per session; the design decisions of `05` P1 |
| P2 | Does offering a subset keep accuracy nearly the same? | **No** | The mechanism question | `allowed_tools` is rejected (`10`); the route left is instruction text without enforcement, which needs its own design |
| P4 | Does masking lower the bill of long runs? | **Not needed yet** | HYP-0021 | Only if P0-P5 show a deployment with large tool results |

## 2. Model independence
Every harness takes the model as a run-time argument and writes it into each output record; no design conclusion may rest on one model (REQ-U22-14). The first items measure the API and the arithmetic, not a model's accuracy: P5 reads token classes, so any model that reports usage will do, and a result is stated as a range across the models the human runs. The third probe's cache question (clean on GLM-5.3, unexplained on gpt-oss and MiniMax-M3) decides which models P5's cached-token readings can be trusted on, so it should be run before or together with P5.

## 3. What I would ask AUTH-020 to cover (draft, for the human to change)
1. **Scope:** write the P5 harness (stdlib Python, no installs) and, after the third probe's output is read, a P3 task set and harness; the human runs them with the key held in the human's own terminal; outputs are stored under `design/package-v5/inputs/` and read by the lead.
2. **Limits:** P5 first, then stop and report before anything else runs; at most about 100 requests per model for P5; the models are the human's choice at run time; no keys, tokens or key identifiers in the workspace; outputs scanned for key material before commit (UTF-8, no redirect); no accuracy claim from P5.
3. **Not covered:** P1, P2 and P4; any change to the design records beyond adding results; any parameter value for the policy; any push other than to `v5-audit`.
4. **Stop rule:** a result that contradicts the arithmetic (D-01, D-04) by more than the run-to-run spread is reported and the design revised before the next item.

## 4. What I can do now without any authorization
Write the P3 task set and catalogue specification (desk work); regenerate the frontier page and sort the 24 "before any implementation" ledger rows under V5; keep records current. None needs the key.
