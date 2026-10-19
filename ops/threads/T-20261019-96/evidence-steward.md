# evidence-steward log, T-20261019-96 (AUTH-010)

No messages sent or received (none required).

## Extractions (python tools/origin_extract.py, all hash verified)
- EXT-0074 r4-anthropic-advanced-tool-use 1-200 (V10)
- EXT-0075 r3-complexmcp 300-460 (V12)
- EXT-0076 r3-tokennotcost 244-258 (V13, extra 1)
- EXT-0077 r3-promcp 466-486 (V13, extra 2)
- EXT-0078 r3-tokennotcost 1600-1612 (V13, extra 3)
- EXT-0079..0082 s4c-g2-dynamicmcpbench-2607-20531 195-240, 380-392, 725-735, 915-930 (V14)
- EXT-0083 same source 975-1060 (V15, V16, V18)
- EXT-0084 s4f-2a-dmcp-dev-e9-1-exposure-matrix 1-110 (V18, extra 4)
Existing extracts re-read: EXT-0008, 0009, 0012, 0023, 0026, 0042, 0060.

## Output
findings/SUM-0004-draft-claims-check.md (id FND-0002), rows V9-V18.

## Not done / limits
- Stub-schema claim (V18) not checked against code or paper text; only the governing digests (second-hand) read.
- Paper outside the listed windows not read (V16: no hier token figure in the windows).
- Claude Code identity and "mostly cache traffic" for the 75% figure rest on STAGE3_CLAIM_LEDGER C3-24 (second-hand).
- verify_workspace.py not run (not required by the task).
