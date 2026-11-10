from math import comb, sqrt
from statistics import NormalDist
Z=NormalDist().inv_cdf
def n_runs(delta,sigma,alpha=.05,power=.8):
    return 2*((Z(1-alpha/2)+Z(power))*sigma/delta)**2
print("paper check: sigma=1.5 delta=2 ->",round(n_runs(2,1.5),2)," delta=1 ->",round(n_runs(1,1.5),2))
# thesis: per-run SD of pass rate on N=57 from identical-run disagreement d tasks
for d in [6,9,12]:
    s=sqrt(57*(d/57)/2)/57*100
    print(f"disagree={d}/57 -> per-run SD of pass rate ~{s:.1f} pts; runs/arm (2-sample, fixed tasks, 80% power, a=.05): "+
      ", ".join(f"delta={D}pt:{n_runs(D,s):.1f}" for D in [2,5,8,10]))
def cp(k,n,a=.05):
    def cdf(x,p): return sum(comb(n,i)*p**i*(1-p)**(n-i) for i in range(0,x+1))
    lo=0;hi=1
    # lower: P(X>=k)=a/2
    L=0.0
    if k>0:
        a_,b_=0,1
        for _ in range(60):
            m=(a_+b_)/2
            if 1-cdf(k-1,m)>a/2: b_=m
            else: a_=m
        L=(a_+b_)/2
    U=1.0
    if k<n:
        a_,b_=0,1
        for _ in range(60):
            m=(a_+b_)/2
            if cdf(k,m)>a/2: a_=m
            else: b_=m
        U=(a_+b_)/2
    return L,U
for b,c in [(7,2),(8,3)]:
    L,U=cp(b,b+c); 
    # net effect = (2p-1)*(b+c) passes
    print(f"b={b},c={c}: exact CP on win share {L:.2f}-{U:.2f}; net passes range {(2*L-1)*(b+c):+.1f}..{(2*U-1)*(b+c):+.1f} (conditional on discordant count)")
