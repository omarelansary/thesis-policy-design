import random, math
random.seed(11)
exec(open('power.py').read().split('for s_task in [0.8')[0])
def boot_ci(d,B=400):
    sums=[sum(d[3*g:3*g+3]) for g in range(G)]
    ms=[]
    for _ in range(B):
        ms.append(sum(sums[random.randrange(G)] for _ in range(G))/N)
    ms.sort(); return ms[int(.025*B)],ms[int(.975*B)]
def trial(shift,K,s_task=3.5,tau=0.7):
    base=draw_world(0.4,1.0,s_task,0)
    inter=[random.gauss(0,tau) for _ in range(N)]
    truediff=sum(sig(base[i]+shift+inter[i])-sig(base[i]) for i in range(N))/N
    a=run_arm(base,0,[0]*N,K); b=run_arm(base,shift,inter,K)
    d=[y-x for x,y in zip(a,b)]
    lo,hi=boot_ci(d)
    return truediff,(lo>0 or hi<0),hi-lo, sum(d)/N
for K in [1,2,4]:
    for shift in [0,0.5,1.0,2.0]:
        R=250; rej=0; w=0; td=0
        for _ in range(R):
            t,r,wd,_e=trial(shift,K); rej+=r; w+=wd; td+=t
        print(f"K={K} logit-shift={shift}: mean true diff={100*td/R:+.1f} pts; CI excludes 0 in {100*rej/R:.0f}% ; mean CI width={100*w/R:.1f} pts (half {50*w/R:.1f})")
