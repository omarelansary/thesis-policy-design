# Evidence layer: what is here, what is not, how to verify it

Snapshot of the origin repository `C:\Users\omr\Documents\research-cleanroom` at commit `67e5eeec4b61` (see `config/origin.json`). The origin remains authoritative. Nothing here was edited; nothing was written to the origin.

**Line numbers.** Everywhere in this workspace a line ends at LF only (a CR before it is dropped), the count that `sed`, `grep -n` and editors give. Python `splitlines()` would also break at form feed and similar characters, which 7 of the stored source texts contain; do not use it to number lines.

## Four kinds of material (never mixed in one file)
| Kind | Where | What it proves |
|---|---|---|
| **Copied source** (byte-exact) | `evidence/governing/<origin path>` + `INDEX.json` (sha256, origin git blob id, last commit date) | That the origin file had these bytes on the snapshot date. Not that its content is true. |
| **Extracted passage** (verbatim) | `evidence/extracts/EXT-NNNN.md` | Exact lines of a source or copy, hash-verified when extracted and re-verifiable by `tools/verify_workspace.py`. |
| **Researcher-generated summary** | files with front matter `type: summary` | Someone's reading. Unverified until checked against EXT. `CAVEATS.md` is an index of pointers, not a summary of conclusions. |
| **New finding** | `findings/FND-*.md` | A claim made in this workspace; must cite EXT ids. |
Generated manifests (`sources.json`, `origin-index.tsv`, `restricted.json`, `governing/INDEX.json`, `config/origin.json`) are immutable except through a human-authorized re-run of `tools/build_origin_snapshot.py`.

## Tiers (see CLAUDE.md)
- **Governing copies (39 files).** Selection rule, stated before looking at any candidate's merits: (1) the approved brief rev. 2 (user decisions and supervisor requirements as read from the 2026-10-02 meeting); (2) all decision records D1-D13; (3) the documents that state the *latest* candidate state and its corrections (S4G brief, S4I erratum and decision sheet, S4D dossier/matrix/quality addendum, S4E/S4F reports and addenda); (4) the final evidence synthesis of each stage (Stage 2 final report, Stage 3 final report and claim ledger, Stage 4 prior-art comparison, Stage 4b map and synthesis, Stage 4c dossier); (5) the audit and correction provenance (integrity-investigation final report, S4H B-1/B-2 reports, S4H closure addendum). Not copied: search logs, per-worker extractions, critic and reviewer reports, per-source L2 tables, operational checkpoints. They are indexed (tier 3) and reachable only with human authorization. The rule is category-based; the copied set contains both documents that favour and documents that qualify each candidate.
- **Source manifests (239).** `sources.json` lists every one, with URL, version, retrieval time, extractor warnings and hashes. No relevance ranking. Of the 239: **232 have stored text** (readable with `tools/origin_extract.py --source ID`), **5 are failed fetches** with no text, and **2 are the fetch tool's own test artefacts** (one has a text file); the fields `has_text` and `kind` say which. For entries with a text file, the manifest's own text hash equals the SHA-256 recomputed on the stored file (checked at snapshot). Some texts are garbled by PDF extraction (two-column tables interleave); quote with care.
- **Origin index (`origin-index.tsv`).** Every tracked origin file outside the stored texts and checkpoints: path, category, size, git blob id, last commit date, and `access` (`copied`, `indexed-only`, `restricted`).

## Withheld and why (`restricted.json`)
- The personal 2026-10-02 transcript (SHA-256 `3c30184741922d849c7c7e6cc30f549fffa8bf9fea45122d8f0e789b4904bc5c`, 507 lines): unpublished and personal; contains student-reported prior-thesis results that stay outside the clean-room boundary.
- `STAGE1_MEETING_RECORD.md` lines 50-66 (student-reported prior work) and the S1 source record. Lines 7-48 (supervisor requirements and assertions) are available as extracts EXT-0003 and EXT-0004.
- The governing copies mention that the student had earlier work (for example "LLM finder", "P1-P9 unverified"); they contain no results of it. If you find any, report it and do not use it.

## Provenance of supervisor material
The 2026-10-02 requirements reach this workspace only through researcher-written records (brief, meeting record) that cite transcript line numbers; the transcript is ASR with garbled product names. A requirement here is "what the clean-room project recorded the supervisor as requiring", not the supervisor's own words, except where a record quotes them. The 2026-10-14 instructions have not been supplied; see `requirements/intake/README.md`.

## Source names: manifest ids and the short names in the governing documents
The governing documents (notably the Stage 3 claim ledger) cite sources by short names such as `r4-github`, `r4-cloudflare`, `r4-speakeasy`; the manifest ids are longer (`r4-github-copilot-fewer-tools`, ...). `tools/origin_extract.py --source` accepts either: exact manifest ids, or a short name listed in `config/source_aliases.json` (44 aliases, 2 groups, derived mechanically on 2026-10-16 by the lead; the governing documents do not state the manifest ids themselves). The tool prints which manifest id an alias resolved to and the extract records `cited_as`. Two aliases resolve to "the only one of several prefix-sharing ids that has stored text" (`r4-speakeasy`, `r2-toolgen`; the other candidates are failed fetches). `s4f-2a-dmcp` and `s4f-2b` denote families and are refused with their member lists. Nothing resolves by silent prefix. Cite the **manifest id** in findings. The line numbers the ledger gives (`L.135` ...) refer to the stored text of the resolved source; four ledger citations were opened and the quoted figures found (assessment of 2026-10-16); that is a spot check, not a verification of every citation.

## Known limits of this layer
- The copies are a snapshot; if the origin moves on, `verify_workspace.py` warns but does not update anything.
- Hashes are over working-tree bytes (CRLF on the origin's Windows checkout); `origin_git_blob12` is the LF-normalised git object for cross-reference.
- Tier-1 selection is a judgement about *categories*, not about claims; a different rule would give a different set. The index lets you see what was left out.
