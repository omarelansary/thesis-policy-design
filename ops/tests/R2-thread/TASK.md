# Thread T-20261016-92: R2 regression (operational, content-neutral; AUTH-001 bootstrap tests)
- Purpose: confirm after the guard hardening that (1) agents can still Read/Glob/Grep inside the workspace, (2) the sanctioned extraction works, (3) messages are counted and the 6th send in a cap-5 thread is refused.
- Bounds: agents = [evidence-steward, design-proposer, design-challenger]; cap 5 (ops/threads/ACTIVE.json); no web; no spawning; no file writes except own thread file.
