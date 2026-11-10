import sys; sys.path.insert(0,'.')
from lib import *
import re,json
TOK=re.compile(r'[A-Za-z0-9_@.\-]+')
def leaves(o,key=''):
    if isinstance(o,dict):
        for k,v in o.items(): yield from leaves(v,k)
    elif isinstance(o,list):
        for v in o: yield from leaves(v,key)
    else: yield key,o
def text(m):
    c=m.get('content'); 
    return c if isinstance(c,str) else json.dumps(c)
TRIV={0,1,'0','1',True,False,None,'',20,'20'}
def analyse(arm):
    T=load(arm); pi,pc,po=[x/1e6 for x in prices(arm)]
    out=dict(n=0,tot=0.0,A=0,B=0,C=0,costA=0.0,costB=0.0,costC=0.0,costtot=0.0,inA=0.0,inB=0.0,inC=0.0,pag=0,fixed=0)
    for t,v in T.items():
        a=[r for r in v if r['ntools']>0]
        for r in a: out['costtot']+=(r['P']-r['C'])*pi+r['C']*pc+r['O']*po
        for r in v:
            if r['ntools']==0: out['costtot']+=0
        seen_fn=set()
        # first request's calls count as seen
        for r in a[:1]:
            for fn,_ in r['args']: seen_fn.add(fn)
        for k in range(1,len(a)):
            r=a[k]; prev=a[k-1]
            if r['ntc']==0: continue
            new_msgs=r['msgs'][prev['nmsg']+1:]   # tool results of previous step
            newtxt=' '.join(text(m) for m in new_msgs if m['role']=='tool')
            oldtxt=' '.join(text(m) for m in r['msgs'][:prev['nmsg']+1])
            newtok=set(TOK.findall(newtxt)); oldtok=set(TOK.findall(oldtxt))
            first_new=newtok-oldtok
            # key:value presence in new results
            kv=set()
            for m in new_msgs:
                if m['role']!='tool': continue
                try:
                    for kk,vv in leaves(json.loads(text(m))): kv.add((kk,str(vv)))
                except Exception: pass
            depA=depB=False  # A claimant-like: new literal; B: + key/value id match
            pag=False
            for fn,argj in r['args']:
                try: ar=json.loads(argj)
                except Exception: ar={}
                for kk,vv in leaves(ar):
                    if vv in TRIV or isinstance(vv,(dict,list)): continue
                    s=str(vv)
                    if s in first_new or any(tk in first_new for tk in TOK.findall(s) if len(tk)>2): depA=True
                    if (kk,s) in kv: depB=True
                if fn in seen_fn and 'page_index' in argj: pag=True
            depC = depA or depB or pag
            c_in=(r['P']-r['C'])*pi+r['C']*pc; c_all=c_in+r['O']*po
            out['n']+=1
            if not depA: out['A']+=1; out['costA']+=c_all; out['inA']+=c_in
            if not (depA or depB): out['B']+=1; out['costB']+=c_all; out['inB']+=c_in
            if not depC: out['C']+=1; out['costC']+=c_all; out['inC']+=c_in
            if pag: out['pag']+=1
            for fn,_ in r['args']: seen_fn.add(fn)
    return out
if __name__=='__main__':
    for arm in ['mm_all','mm_sub','glm_all','glm_sub']:
        o=analyse(arm); n=o['n']
        print(arm,'steps>=2nd %d'%n,'indep(A literal-only) %.0f%% | (B +kv id) %.0f%% | (C +pagination) %.0f%% | pag-cont %.0f%%'%(100*o['A']/n,100*o['B']/n,100*o['C']/n,100*o['pag']/n),
          '|| bill share if whole request removed A/B/C: %.0f/%.0f/%.0f%%; input-side only: %.0f/%.0f/%.0f%%'%tuple(100*x/o['costtot'] for x in [o['costA'],o['costB'],o['costC'],o['inA'],o['inB'],o['inC']]))
