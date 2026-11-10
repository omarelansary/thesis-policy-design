import random, math, itertools
random.seed(1)
try:
    import numpy as np
    HAVE=True
except Exception:
    HAVE=False
print("numpy",HAVE)
from math import comb
# --- part 1: observed-style data: 57 tasks, 19 clusters of 3; single run pair; b=wins A, c=wins B
def mcnemar_exact(b,c):
    n=b+c; k=min(b,c)
    p=sum(comb(n,i) for i in range(0,k+1))/2**n*2
    return min(1,p)
def cluster_boot(d, clusters, B=20000):
    # d: list of per-task diffs (in passes), clusters: list of lists idx
    G=len(clusters); means=[]
    sums=[sum(d[i] for i in c) for c in clusters]
    for _ in range(B):
        s=0
        for _ in range(G): s+=sums[random.randrange(G)]
        means.append(s)
    means.sort()
    return means[int(.025*B)],means[int(.975*B)]
def cluster_signflip(sums):
    # exact randomisation test over 2^G sign flips of cluster sums (G=19 -> 524288)
    G=len(sums); obs=abs(sum(sums)); cnt=0; tot=0
    # DP over distribution of sums (integers or half-integers) 
    from collections import Counter
    dist=Counter({0:1})
    for s in sums:
        nd=Counter()
        for k,v in dist.items():
            nd[k+s]+=v; nd[k-s]+=v
        dist=nd
    tot=2**G
    cnt=sum(v for k,v in dist.items() if abs(k)>=obs-1e-9)
    return cnt/tot
def wilson_paired(b,c,n):
    # Wilson CI on discordant split then convert? use Newcombe/ Tango-like: skip
    pass
clusters=[[3*g,3*g+1,3*g+2] for g in range(19)]
def make_d(b,c,placement):
    n=57
    idx=list(range(n))
    if placement=="random":
        random.shuffle(idx)
        pos=idx[:b]; neg=idx[b:b+c]
    elif placement=="concentrated":
        # discordants fill whole clusters: order tasks by cluster, same sign tendency within cluster
        pos=[];neg=[]
        order=list(range(n)); 
        # put positives in first clusters, negatives in later ones, contiguous
        pos=order[:b]; neg=order[b:b+c]
    d=[0]*n
    for i in pos:d[i]=1
    for i in neg:d[i]=-1
    return d
print("== observed-style scenarios, net +5 passes (out of 57), single run each arm ==")
for b,c in [(7,2),(8,3),(9,4)]:
    print(f"b={b} c={c} discordant={b+c} net={b-c} McNemar exact p={mcnemar_exact(b,c):.3f}")
    for pl in ["random","concentrated"]:
        d=make_d(b,c,pl)
        lo,hi=cluster_boot(d,clusters)
        sums=[sum(d[i] for i in cl) for cl in clusters]
        p=cluster_signflip(sums)
        # naive paired SE
        n=57; m=sum(d)/n; sd=(sum((x-m)**2 for x in d)/(n-1))**.5; se=sd/n**.5
        # clustered SE (Miller eq 4 style)
        cs=[sum(x-m for x in [d[i] for i in cl]) for cl in clusters]
        secl=(sum(s*s for s in cs))**.5/n
        print(f"  {pl:12s} naive 95% CI on net passes: {(m-1.96*se)*n:+.1f}..{(m+1.96*se)*n:+.1f}; clustered-SE CI: {(m-1.96*secl)*n:+.1f}..{(m+1.96*secl)*n:+.1f}; cluster-boot: {lo:+.0f}..{hi:+.0f} ; cluster sign-flip p={p:.3f}")
