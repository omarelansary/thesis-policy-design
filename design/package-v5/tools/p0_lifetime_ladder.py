"""Runs the cache-lifetime ladder of p0_api_probe_v3.py --mode lifetime unattended (RUN BY THE HUMAN, not by the lead).

The key is asked once with hidden input (getpass), kept only in this process's memory and passed to the probe through the
child process's environment; it is never printed or written. Each round sends one base request per model (the same
command as by hand) and appends one line to that model's file; then the script waits for the next gap, measured from
the previous round, because a warm read may renew the cache. Default gaps: 30, 60, 120, 240 minutes (about 7.5 hours).

The computer must stay on and awake (no sleep or hibernation) and this terminal must stay open. Stop any time with Ctrl+C;
the rounds already done are kept.

PowerShell:
    python design/package-v5/tools/p0_lifetime_ladder.py
    python design/package-v5/tools/p0_lifetime_ladder.py --gaps 30,60,90,120     # a shorter ladder (5 hours)
"""
import argparse, datetime, getpass, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = os.path.join(HERE, "p0_api_probe_v3.py")
INPUTS = os.path.join(os.path.dirname(HERE), "inputs")
MODELS = {"openai/gpt-oss-120b": "p0-api-lifetime.jsonl",
          "MiniMaxAI/MiniMax-M3": "p0-api-minmax-lifetime.jsonl",
          "zai-org/GLM-5.3": "p0-api-glm-lifetime.jsonl"}

ap = argparse.ArgumentParser()
ap.add_argument("--gaps", default="30,60,120,240", help="minutes to wait before each round, measured from the previous round")
a = ap.parse_args()
gaps = [float(x) for x in a.gaps.split(",") if x.strip()]

key = getpass.getpass("SCADS API key (input hidden): ").strip()
if not key:
    sys.exit("No key entered. Nothing was sent.")
env = dict(os.environ, SCADS_API_KEY=key)


def now():
    return datetime.datetime.now().strftime("%H:%M")


def last_cached(path):
    try:
        with open(path, encoding="utf-8") as f:
            rec = json.loads(f.read().splitlines()[-1])
    except (OSError, ValueError, IndexError):
        return "?"
    for v in rec.values():
        if isinstance(v, dict) and "V0_base" in v:
            u = (v["V0_base"].get("usage") or {})
            d = u.get("prompt_tokens_details") or {}
            return f"{d.get('cached_tokens')} of {u.get('prompt_tokens')} cached"
    return "?"


print(f"{now()} ladder started: {len(gaps)} rounds after gaps of {', '.join(f'{g:g}' for g in gaps)} minutes; keep this terminal open.")
try:
    for i, g in enumerate(gaps, 1):
        wake = datetime.datetime.now() + datetime.timedelta(minutes=g)
        print(f"{now()} waiting {g:g} min for round {i} (at about {wake.strftime('%H:%M')})", flush=True)
        time.sleep(g * 60)
        for model, fname in MODELS.items():
            out = os.path.join(INPUTS, fname)
            r = subprocess.run([sys.executable, PROBE, "--mode", "lifetime", "--model", model, "--out", out],
                               env=env, capture_output=True, text=True, timeout=600)
            status = last_cached(out) if r.returncode == 0 else f"probe failed (exit {r.returncode})"
            print(f"{now()} round {i}, gap {g:g} min, {model}: {status}", flush=True)
except KeyboardInterrupt:
    print(f"\n{now()} stopped by you; the rounds already done are in the files.")
finally:
    key = env = None
print(f"{now()} ladder finished. Tell the lead 'done'.")
