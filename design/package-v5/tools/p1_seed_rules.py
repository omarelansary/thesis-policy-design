"""P1 step A (AUTH-033, 2026-11-10): seed rules for AppWorld's returning users, compared on gold, no model request.
Each rule picks seeds from the user's history only (no look at the current task). Per returning session: seeds m, needed seeds
n (in this session's required non-core APIs), precision h = n/m, recall = n / non-core needs. Bill effect by calc/memory_seed.py
revision 4 (client-side search): net = n*saving - (m-n)*cost, in fresh-input-token equivalents per session, for K matches per
search, cache-read ratio r and session length T. Counts only printed.
Rules: all (every API needed before), ge2 (needed in two or more earlier sessions), last (the most recent earlier session only),
pop6 (the six non-core APIs most often needed by other users' sessions outside the current scenario, a role memory), app2 (all APIs of the apps the user
needed in two or more earlier sessions: needs the API list per app, from the tasks' required APIs).
Usage: python3 -I design/package-v5/tools/p1_seed_rules.py ~/r3-work/aw-root/data
"""
import collections, contextlib, importlib.util, io, json, os, pathlib, statistics, sys

DATA = os.path.expanduser(sys.argv[1])
CALC = pathlib.Path(__file__).resolve().parent.parent / "calc" / "memory_seed.py"
spec = importlib.util.spec_from_file_location("ms", CALC); ms = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(ms)
ids = []
for split in ("train", "dev"):
    ids += [l.strip() for l in open(os.path.join(DATA, "datasets", f"{split}.txt")) if l.strip()]
core = lambda a: a.split(".")[0] == "supervisor" or a.split(".")[-1] == "login"
users = {}
for t in ids:
    s = json.load(open(os.path.join(DATA, "tasks", t, "specs.json")))
    apis = {a for a in json.load(open(os.path.join(DATA, "tasks", t, "ground_truth", "required_apis.json"))) if not core(a)}
    users.setdefault(s["supervisor"]["email"], {}).setdefault(t.split("_")[0], (s["datetime"], t, apis))
sessions = {u: sorted(sc.values()) for u, sc in users.items()}
app_apis = collections.defaultdict(set)
for u, ss in sessions.items():
    for _, _, a in ss:
        for x in a:
            app_apis[x.split(".")[0]].add(x)


def pop6(u, scen):
    # other users' sessions, excluding every task of the current session's scenario (its sibling tasks need nearly the same APIs)
    c = collections.Counter(a for v, ss in sessions.items() if v != u for _, t, aa in ss if t.split("_")[0] != scen for a in aa)
    return {a for a, _ in c.most_common(6)}


def seeds(rule, u, hist, scen=None):
    if rule == "all":
        return set().union(*(h[2] for h in hist))
    if rule == "ge2":
        c = collections.Counter(a for h in hist for a in h[2]); return {a for a, k in c.items() if k >= 2}
    if rule == "last":
        return set(hist[-1][2])
    if rule == "pop6":
        return pop6(u, scen)
    if rule == "app2":
        c = collections.Counter(app for h in hist for app in {a.split(".")[0] for a in h[2]})
        return set().union(*(app_apis[a] for a, k in c.items() if k >= 2)) if any(k >= 2 for k in c.values()) else set()


def econ(t, r, k):
    s = (ms.H + ms.P) * r + ms.O * ms.Q
    return s + (k - 1) * ms.D * (ms.W + (t / 2) * r) - ms.D * r * ((t - 1) - t / 2), ms.D * (ms.W + (t - 1) * r)


print(f"{'rule':5} {'sessions with seeds':>19} {'mean m':>7} {'mean h':>7} {'mean recall':>11} | net per returning session (fresh-token eq.), and sessions with h >= h*")
for rule in ("all", "ge2", "last", "pop6", "app2"):
    rows = []
    for u, ss in sessions.items():
        for i in range(1, len(ss)):
            sd = seeds(rule, u, ss[:i], ss[i][1].split("_")[0]); now = ss[i][2]; n = len(sd & now)
            rows.append((len(sd), n, len(now)))
    withs = [r for r in rows if r[0]]
    mh = statistics.mean(r[1] / r[0] for r in withs) if withs else 0
    rec = statistics.mean(r[1] / r[2] if r[2] else 0 for r in rows)
    cells = []
    for (k, r, t) in ((3, 0.1, 8), (1, 0.1, 8), (3, 0.1, 30)):
        sv, cs = econ(t, r, k); hstar = ms.hstar(t, r, "client", k)
        net = statistics.mean(n * sv - (m - n) * cs for m, n, _ in rows)
        over = sum(1 for m, n, _ in withs if n / m >= hstar)
        cells.append(f"K={k},T={t}: {net:+7.0f}, {over}/{len(rows)}")
    print(f"{rule:5} {len(withs):>12}/{len(rows):<6} {statistics.mean(r[0] for r in rows):>7.1f} {mh:>7.2f} {rec:>11.2f} | " + "; ".join(cells))
sv, cs = econ(8, 0.1, 3)
print(f"\nper needed seed saving {sv:.0f}, per unneeded seed cost {cs:.0f} (K=3, T=8, r=0.1); a whole 8-request session of P2's size bills roughly 50,000 (approximate)")
