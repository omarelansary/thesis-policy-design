# Intake rules for new supervisor or user material

Used for the 2026-10-14 supervisor instructions and for any later supervisor, user or advisor input.

1. **Store verbatim first.** Save the text exactly as supplied in `requirements/intake/<YYYY-MM-DD>-<source>.md` with a header block: who supplied it, when, in what form (transcript, notes, message), what the supplier says it is, SHA-256 of the stored text, and any known transcription caveats. Do not edit it afterwards; corrections are new files.
2. **Classify each statement** in a separate register entry (add to `requirements/REGISTER.md`, new REQ id): `supervisor-requirement` (stated as an instruction or condition), `supervisor-example` (explicitly illustrative), `supervisor-assertion` (an empirical claim to test), `user-decision`, or `unclear` (ask). Keep the supervisor's words in an EXT extract; the register carries a pointer, not a paraphrase.
3. **Never present intake material as evidence.** A supervisor instruction is a requirement; a supervisor example is an illustration; a supervisor assertion is a claim awaiting evidence. None is an "independently established scientific finding" and none goes under `evidence/governing/`.
4. **Contradictions with earlier requirements are recorded, not resolved** by an agent: add a note in the register pointing to both sides and put the question to the human.
5. **Previous-thesis experimental content** that appears in supplied material stays out: describe it as withheld in the register, do not copy it into any other file.
6. Only the human decides whether new material supersedes an earlier requirement, and records that in `ops/AUTHORIZATIONS.md` / `ops/DESIGN-DECISIONS.md`.
