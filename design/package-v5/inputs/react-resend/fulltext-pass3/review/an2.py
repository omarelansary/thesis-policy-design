import json,glob,os,statistics as st
os.chdir('/home/omar/r3-work/runs')
runs={'mm3-b2r-repeat':(0.24,0.96,0.048),'glm-b2-control':(0.70,2.20,0.13),'glm-b2-control-rest':(0.70,2.20,0.13)}
agg={}
for r,(pf,po,pc) in runs.items():
    key='MM' if r.startswith('mm') else 'GLM'
    a=agg.setdefault(key,dict(pred=0,pre_c=0,pre_f=0,hist_c=0,hist_f=0,out=0,n=0,P0=[],agentreq=0))
    for f in glob.glob(f'{r}/experiments/outputs/*/tasks/*/logs/lm_calls.jsonl'):
        rows=[json.loads(l) for l in open(f)]
        if len(rows)<2: continue
        a['n']+=1
        for i,d in enumerate(rows):
            u=d['output'].get('usage') or {}
            pt=u.get('prompt_tokens',0); c=(u.get('prompt_tokens_details') or {}).get('cached_tokens',0) or 0; ct=u.get('completion_tokens',0)
            if i==0:
                a['pred']+=((pt-c)*pf+c*pc+ct*po); continue
            if i==1: P0=pt; a['P0'].append(pt)
            a['agentreq']+=1
            pre_c=min(c,P0); hist_c=c-pre_c; pre_f=P0-pre_c; hist_f=pt-P0-hist_c
            a['pre_c']+=pre_c*pc;a['pre_f']+=pre_f*pf;a['hist_c']+=hist_c*pc;a['hist_f']+=hist_f*pf;a['out']+=ct*po
for k,a in agg.items():
    T=sum(a[x] for x in('pred','pre_c','pre_f','hist_c','hist_f','out'))
    print(k,a['n'],'total $%.2f'%(T/1e6),{x:'%.0f%%'%(100*a[x]/T) for x in('pred','pre_c','pre_f','hist_c','hist_f','out')},'agent P0 mean %.0f'%st.mean(a['P0']),'agent reqs/task %.1f'%(a['agentreq']/a['n']))
