"""P1 desk check (2026-11-10): recurrence of needed APIs for AppWorld's returning users, and the seed precision h of HYP-0017's
falsifier against the break-even h* of calc/memory_seed.py (revision 4). No model request. Prints counts only (no user identity,
task text or API name). Rebuilds the table of inputs/p1/P1-PREP.md section 2, whose script was not kept, and checks it.
Users = supervisors (by email) of the train and dev tasks; one task per scenario per user (the first by id); sessions in date
order; a returning session is every session after the first. Core = the supervisor app and every login API (always offered).
Seeds = all non-core APIs needed in the user's earlier sessions. h (precision) = share of seeds this session needs; recall =
share of this session's non-core needs that were seeds.
Usage: python3 -I design/package-v5/tools/p1_recurrence.py ~/r3-work/aw-root/data
"""
import contextlib, importlib.util, io, json, os, pathlib, statistics, sys

DATA = os.path.expanduser(sys.argv[1])
CALC = pathlib.Path(__file__).resolve().parent.parent / "calc" / "memory_seed.py"
ids = []
for split in ("train", "dev"):
    ids += [l.strip() for l in open(os.path.join(DATA, "datasets", f"{split}.txt")) if l.strip()]
users = {}
for t in ids:
    s = json.load(open(os.path.join(DATA, "tasks", t, "specs.json")))
    apis = set(json.load(open(os.path.join(DATA, "tasks", t, "ground_truth", "required_apis.json"))))
    users.setdefault(s["supervisor"]["email"], {}).setdefault(t.split("_")[0], (s["datetime"], t, apis))
core = lambda a: a.split(".")[0] == "supervisor" or a.split(".")[-1] == "login"
rows = []
for u, sc in users.items():
    sess = sorted(sc.values())
    for i in range(1, len(sess)):
        prev_all = set().union(*(x[2] for x in sess[:i])); now_all = sess[i][2]
        prev = {a for a in prev_all if not core(a)}; now = {a for a in now_all if not core(a)}
        rows.append(dict(rec_all=len(now_all & prev_all) / len(now_all), prec_all=len(now_all & prev_all) / len(prev_all),
                         rec=len(now & prev) / len(now) if now else 0.0, h=len(now & prev) / len(prev) if prev else 0.0,
                         seeds=len(prev)))
ret = [u for u, sc in users.items() if len(sc) >= 2]
q = lambda v: [round(x, 2) for x in statistics.quantiles(v, n=4)]
print(f"tasks {len(ids)}, users {len(users)}, returning users {len(ret)}, returning sessions {len(rows)}")
print("sessions per returning user:", {k: sum(len(users[u]) == k for u in ret) for k in range(2, 6)})
for k, lab in (("rec_all", "recall, all APIs"), ("prec_all", "precision, all APIs"), ("rec", "recall, non-core"), ("h", "precision h, non-core")):
    v = [r[k] for r in rows]
    print(f"{lab}: mean {statistics.mean(v):.2f}, quartiles {q(v)}, zero in {sum(x == 0 for x in v)}, one in {sum(x == 1 for x in v)}")
print("seed set size (non-core), median", statistics.median(r["seeds"] for r in rows))

spec = importlib.util.spec_from_file_location("ms", CALC)
ms = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(ms)
hs = [r["h"] for r in rows]
print("\nreturning sessions whose h reaches h* (client-side search; T = requests per session; P2 median T = 8):")
for k in (1, 3):
    for r in (0.1, 0.05, 0.025):
        cells = []
        for t in (3, 8, 10, 30):
            hstar = ms.hstar(t, r, "client", k)
            cells.append(f"T={t}: h*={'never' if hstar is None else f'{hstar:.2f}'} -> {0 if hstar is None else sum(h >= hstar for h in hs)}/{len(hs)}")
        print(f"  K={k} r={r}: " + "; ".join(cells))
