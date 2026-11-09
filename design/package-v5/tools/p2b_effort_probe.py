"""P2b (INT-T-050): reasoning tokens of GLM-5.3 on OpenRouter GMICloud with no effort sent, low and high (2 each), and the key credit.
Run 2026-11-09: none 236/421, low 50/73, high 224/172 reasoning tokens; $0.004. Key from the environment, never printed."""
import json, os, urllib.request
K = os.environ["OPENROUTER_API_KEY"]
def req(url, body=None):
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                               headers={"Authorization": f"Bearer {K}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=600))
k = req("https://openrouter.ai/api/v1/key")["data"]
print("credit: usage", k.get("usage"), "limit", k.get("limit"), "remaining", k.get("limit_remaining"))
Q = "A shop sells pens at 3 for $2 and notebooks at 2 for $5. I buy 7 pens and 5 notebooks. Each item is sold only in whole packs. What is the least I pay? Answer with the number."
tot = 0
for setting in (None, "low", "high"):
    for rep in (1, 2):
        b = {"model": "z-ai/glm-5.3", "messages": [{"role": "user", "content": Q}], "temperature": 0, "seed": 100,
             "provider": {"order": ["GMICloud"], "allow_fallbacks": False}, "usage": {"include": True}}
        if setting: b["reasoning"] = {"effort": setting}
        j = req("https://openrouter.ai/api/v1/chat/completions", b)
        u = j["usage"]; tot += u.get("cost") or 0
        print(setting or "none sent", rep, "provider", j.get("provider"), "reasoning tokens", (u.get("completion_tokens_details") or {}).get("reasoning_tokens"),
              "completion", u.get("completion_tokens"), "cost", u.get("cost"))
print("probe cost", round(tot, 5))
