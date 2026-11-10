import random, math
random.seed(7)
def sig(x): return 1/(1+math.exp(-x))
G=19; M=3; N=57
def draw_world(mu, s_cl, s_task, s_arm):
    base=[]; 
    for g in range(G):
        u=random.gauss(0,s_cl)
        for m in range(M):
            base.append(mu+u+random.gauss(0,s_task))
    return base
def run_arm(base, shift, inter, K):
    # inter: per-task arm interaction (fixed per world)
    res=[]
    for i in range(N):
        p=sig(base[i]+shift+inter[i])
        res.append(sum(1 if random.random()<p else 0 for _ in range(K))/K)
    return res
def disagreement(mu,s_cl,s_task,reps=300):
    t=0
    for _ in range(reps):
        b=draw_world(mu,s_cl,s_task,0)
        a=run_arm(b,0,[0]*N,1); c=run_arm(b,0,[0]*N,1)
        t+=sum(1 for x,y in zip(a,c) if x!=y)
    return t/reps
for s_task in [0.8,1.2,1.6,2.0]:
    print("s_task",s_task,"identical-run disagreements/57 =",round(disagreement(0.4,1.0,s_task),1))
print("--- calibrate")
for s_task in [2.5,3.0,3.5,4.0]:
    print("s_task",s_task,round(disagreement(0.4,1.0,s_task),1))
