import json,glob,os
R='/home/omar/r3-work/runs/'
PR={'mm':(0.24,0.048,0.96),'glm':(0.70,0.13,2.20)}
def task_files(run):
    d={}
    for p in glob.glob(R+run+'/experiments/outputs/*/tasks/*/logs/lm_calls.jsonl'):
        d[p.split('/tasks/')[1].split('/')[0]]=p
    return d
def load(arm):
    runs={'mm_all':['mm3-b1r-repeat'],'mm_sub':['mm3-b2r-repeat'],'glm_all':['glm-b1-all-tools'],'glm_sub':['glm-b2-control','glm-b2-control-rest']}[arm]
    files={}
    for r in runs: files.update(task_files(r))   # later run overrides
    tasks={}
    for t,p in files.items():
        reqs=[]
        for l in open(p):
            d=json.loads(l); u=d['output']['usage']; m=d['output']['choices'][0]['message']
            tcs=m.get('tool_calls') or []
            reqs.append(dict(P=u['prompt_tokens'],C=min((u.get('prompt_tokens_details') or {}).get('cached_tokens') or 0,u['prompt_tokens']),O=u['completion_tokens'],
              ntools=len(d['input'].get('tools') or []),nmsg=len(d['input']['messages']),ntc=len(tcs),cost=u.get('cost'),
              args=[(c['function']['name'],c['function']['arguments']) for c in tcs],msgs=d['input']['messages'],content=m.get('content')))
        tasks[t]=reqs
    return tasks
def prices(arm): return PR[arm.split('_')[0]]
