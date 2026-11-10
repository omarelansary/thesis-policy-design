# ReAct re-send cost: independent assessment, supporting files (2026-11-09 / 10)

Question: what does the supervisor's concern (every ReAct tool call is another model request that re-sends the same input)
reveal about the V5 tool-exposure research? Written by Claude (Sonnet 5.5) as research owner, at the human's request.
Nothing here is an authorization, a validated finding or a change to the V5 policy. No paid run was made.

## What is here
- ASSESSMENT.md (add by exporting the Claude Docs document "ReAct re-send cost: independent assessment" to Markdown):
  the decision-ready assessment, sections 1-9. The living copy is in Claude Docs.
- analysis/            first-pass scripts on the stored R3 per-request logs (cost anatomy, trace audit, bounds).
                       bill_components.py is the corrected version; the *_SUPERSEDED_* file keeps the earlier
                       version for audit (it used the predictor call as the prefix for subset arms).
- literature/          first-pass literature investigator report.
- replication/         blind re-derivation of the first-pass numbers by a second agent, with its code and critique.
- literature-pass2/    seven lane reports (serving, cost methodology, tool selection, call reduction, context
                       management, provider pricing, benchmarks) plus a coverage critic; each lane has
                       queries.tsv, sources.tsv, excluded.tsv; VERIFICATION_LEDGER.tsv holds my own checks.
- fulltext-pass3/      full-text verification of 31 sources: FULLTEXT_VERIFICATION_LEDGER.tsv (per paper),
                       reports/ (four readers), review/ (adversarial review and its scripts),
                       final-checks/ (final_checks.py and a blind replication), CHANGELOG.md (what changed and why).

## Provenance and caveats
- Raw data are NOT included: per-request logs live in ~/r3-work/runs/ (git-excluded, 1.8 GB); scripts read them from there.
- Downloaded papers are NOT included (untrusted, bulky). arXiv ids are in the ledgers; fulltext-pass3/code/fetch_arxiv.sh re-fetches them.
- Reports by delegated researchers are model output, spot-checked or fully verified as stated in the ledgers; read the
  ledger status column before citing any number from them.
- Headline numbers to cite only with their conditions: see section 9.6 of the assessment (step-capped runs, cold-start).
- Key reproducible check: cd ~/r3-work/runs && python3 -I <this folder>/fulltext-pass3/final-checks/final_checks.py
