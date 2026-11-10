import random,math
random.seed(1)
def binom(n,p): return sum(random.random()<p for _ in range(n))
def sim(d,k,tau,rho,nsim=300,B=200):
    m=2*d; base=[0.5]*m+[1.0]*(57-m-8)+[0.0]*8   # 8 impossible tasks
    cl=[i//3 for i in range(57)]
    hws=[];ests=[]
    for _ in range(nsim):
        uc=[random.gauss(0,1) for _ in range(19)]
        pB=[]
        for i,b in enumerate(base):
            if 0<b<1:
                u=math.sqrt(rho)*uc[cl[i]]+math.sqrt(1-rho)*random.gauss(0,1)
                pB.append(min(.98,max(.02,b+tau*u)))
            else: pB.append(b)
        diff=[(binom(k,pB[i])-binom(k,base[i]))/k for i in range(57)]
        cd=[sum(diff[3*c:3*c+3]) for c in range(19)]
        ests.append(sum(cd)/57)
        bs=sorted(sum(cd[random.randrange(19)] for _ in range(19))/57 for _ in range(B))
        hws.append((bs[int(.975*B)]-bs[int(.025*B)])/2)
    return 100*sum(hws)/len(hws), 100*(sum(e*e for e in ests)/len(ests))**.5
for d in (6,12):
    for tau,rho in ((0,0),(0.15,0),(0.15,0.5)):
        print('d=%d tau=%.2f rho=%.1f '%(d,tau,rho),' | '.join('k=%d: half-width +-%.1f (SD of est %.1f)'%((k,)+sim(d,k,tau,rho)) for k in (1,2,4)))
