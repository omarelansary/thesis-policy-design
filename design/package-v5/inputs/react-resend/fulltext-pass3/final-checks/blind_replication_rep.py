import json,glob,os,sys
R='/home/omar/r3-work/runs/'
P={'mm':(0.24,0.96,0.048),'glm':(0.70,2.20,0.13)}
def load(runs,pk):
    f,o,c=P[pk]; T={}
    for run in runs:
        for p in sorted(glob.glob(R+run+'/experiments/outputs/*/tasks/*/logs/lm_calls.jsonl')):
            tid=p.split('/tasks/')[1].split('/')[0]
            reqs=[]
            for line in open(p):
                line=line.strip()
                if not line: continue
                d=json.loads(line); u=d['output'].get('usage') or {}
                pt=u.get('prompt_tokens',0); ct=u.get('completion_tokens',0)
                ca=((u.get('prompt_tokens_details') or {}).get('cached_tokens')) or 0
                reqs.append(dict(agent=d['input'].get('tools') is not None,pt=pt,ct=ct,ca=ca))
            T[tid]=(run,reqs)   # later run wins
    out={}
    for tid,(run,reqs) in T.items():
        ag=[r for r in reqs if r['agent']]; pr=[r for r in reqs if not r['agent']]
        def cost(r): return ((r['pt']-r['ca'])*f+r['ca']*c+r['ct']*o)/1e6
        t=dict(run=run,n=len(ag),ag=ag,pr=pr,cost=sum(map(cost,reqs)),ptok=sum(r['pt'] for r in reqs),capped=len(ag)>=48)
        # cold
        if ag:
            a=ag[0]; t['cold']=a['ca']*(f-c)/1e6
        else: t['cold']=0
        # anatomy
        pre=hist=0;prc=hic=0
        pf=pc=hf=hc=0
        prefix_len=ag[0]['pt'] if ag else 0
        for r in ag:
            pre_tok=min(prefix_len,r['pt']); 
            cached_in_pre=min(r['ca'],pre_tok); cached_in_hist=r['ca']-cached_in_pre
            pre_fresh=pre_tok-cached_in_pre; hist_fresh=(r['pt']-pre_tok)-cached_in_hist
            pf+=pre_fresh;pc+=cached_in_pre;hf+=hist_fresh;hc+=cached_in_hist
        t['pre']=(pf*f+pc*c)/1e6; t['hist']=(hf*f+hc*c)/1e6
        t['out']=sum(r['ct']*o for r in ag)/1e6
        t['pred']=sum(map(cost,pr))
        out[tid]=t
    return out
arms={'MM all':(['mm3-b1r-repeat'],'mm'),'MM sub':(['mm3-b2r-repeat'],'mm'),'GLM all':(['glm-b1-all-tools'],'glm'),'GLM sub':(['glm-b2-control','glm-b2-control-rest'],'glm')}
D={k:load(*v) for k,v in arms.items()}
for k,d in D.items():
    tot=sum(t['cost'] for t in d.values()); tp=sum(t['ptok'] for t in d.values())
    cap=[t for t in d.values() if t['capped']]
    print(k,'tasks',len(d),'total',round(tot,3),'capped',len(cap),'bill%',round(100*sum(t['cost'] for t in cap)/tot,1),'tok%',round(100*sum(t['ptok'] for t in cap)/tp,1),
      'cold+%',round(100*sum(t['cold'] for t in d.values())/tot,2),'maxn',max(t['n'] for t in d.values()), 'n>=45',sum(t['n']>=45 for t in d.values()))
    nc=[t for t in d.values() if not t['capped']]
    s=sum(t['cost'] for t in nc)
    if 'sub' in k:
        print('  anatomy(no capped): ',{x:round(100*sum(t[x] for t in nc)/s,1) for x in ['pre','hist','out','pred']}, 'sum check',round(sum(t['pre']+t['hist']+t['out']+t['pred'] for t in nc)/s,4))
    if 'GLM sub' ==k: print(' by run',{r:sum(1 for t in d.values() if t['run']==r) for r in set(t['run'] for t in d.values())})
for m in ['MM','GLM']:
    A,S=D[m+' all'],D[m+' sub']
    common=sorted(set(A)&set(S))
    print(m,'common',len(common),'only all',len(set(A)-set(S)),'only sub',len(set(S)-set(A)))
    print(' mean ratio all tasks',sum(A[t]['cost']/S[t]['cost'] for t in common)/len(common))
    c2=[t for t in common if not A[t]['capped'] and not S[t]['capped']]
    print(' both-uncapped',len(c2),sum(A[t]['cost']/S[t]['cost'] for t in c2)/len(c2))
    # each-arm removed: ratio of per-task means
    ua=[A[t]['cost'] for t in A if not A[t]['capped']]; us=[S[t]['cost'] for t in S if not S[t]['capped']]
    print(' ratio of arm means (capped removed per arm)',(sum(ua)/len(ua))/(sum(us)/len(us)),len(ua),len(us))
    print(' ratio of totals',sum(t['cost'] for t in A.values())/sum(t['cost'] for t in S.values()))
