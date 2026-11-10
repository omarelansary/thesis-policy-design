import json,glob,sys,statistics as st,os
os.chdir('/home/omar/r3-work/runs')
runs={'mm3-b1r-repeat':(0.24,0.96,0.048),'mm3-b2r-repeat':(0.24,0.96,0.048),'glm-b1-all-tools':(0.70,2.20,0.13),'glm-b2-control':(0.70,2.20,0.13),'glm-b2-control-rest':(0.70,2.20,0.13)}
for r,(pf,po,pc) in runs.items():
    tot=dict(pre_c=0,pre_f=0,hist_c=0,hist_f=0,out=0); n=0;reqs=0;first=[];toolch=[];msgch=[];ntools=set();firstcached=[]
    for f in glob.glob(f'{r}/experiments/outputs/*/tasks/*/logs/lm_calls.jsonl'):
        rows=[json.loads(l) for l in open(f)]
        if not rows: continue
        n+=1
        P0=None
        for i,d in enumerate(rows):
            u=d['output'].get('usage') or {}
            pt=u.get('prompt_tokens',0); c=(u.get('prompt_tokens_details') or {}).get('cached_tokens',0) or 0
            ct=u.get('completion_tokens',0)
            if i==0:
                P0=pt; first.append(pt); firstcached.append(c)
                toolch.append(len(json.dumps(d['input'].get('tools'))));msgch.append(len(json.dumps(d['input']['messages'])))
                ntools.add(len(d['input'].get('tools') or []))
            pre_c=min(c,P0); hist_c=c-pre_c
            pre_f=P0-pre_c; hist_f=(pt-P0)-hist_c
            tot['pre_c']+=pre_c*pc;tot['pre_f']+=pre_f*pf;tot['hist_c']+=hist_c*pc;tot['hist_f']+=hist_f*pf;tot['out']+=ct*po
            reqs+=1
    T=sum(tot.values())/1e6
    print(r,'tasks',n,'reqs/task %.1f'%(reqs/n),'bill $%.2f'%T,{k:'%.0f%%'%(100*v/1e6/T) for k,v in tot.items()},'\n  first prompt mean %.0f'%st.mean(first),'first cached mean %.0f'%st.mean(firstcached),'ntools',ntools,'tools chars frac %.3f'%(st.mean(toolch)/(st.mean(toolch)+st.mean(msgch))), 'msgchars %.0f toolchars %.0f'%(st.mean(msgch),st.mean(toolch)))
