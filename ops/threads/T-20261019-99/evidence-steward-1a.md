# Steward 1a log (written by the lead from the steward's hand-back; the guard blocked the steward's own write)
- Findings: findings/SUM-0010-batch1a-provider-docs.md (FND-0008). No messages sent.
- Extractions: EXT-0115 (anthropic prompt caching 606-656), EXT-0123 (1770-1806), EXT-0131 (anthropic tool search 760-840), EXT-0137 (bedrock 55-85), EXT-0141 (gemini caching 340-380), EXT-0142 (openai prompt caching 48-116), EXT-0143 (MCP caching spec 1-177), EXT-0144 (anthropic ptc 30-60), EXT-0145 (openai tool search 60-80).
- Verdicts: N-5 and N-5/UNREAD PARTLY; C-S03/MINCACHE PARTLY; C-S03/EXCEPTIONS PARTLY (ten cases); C-S03/DEFUSAGE PARTLY; N-26 mechanisms documented; C-E02/E22 PARTLY.
- Contradictions of the ledger wording: Bedrock minimum starts at 512 (not 1,024); "not stated" wrong for Anthropic loaded definitions; the one-full-miss exception is tied to the inline-tools beta; no hourly storage statement in the ranges read.
- Not read: rest of each page; Anthropic 1-hour option and minimums; Gemini explicit caching; the 'Tool use with prompt caching' page.
