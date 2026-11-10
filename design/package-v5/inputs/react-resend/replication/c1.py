import sys; sys.path.insert(0,'.')
from lib import *
import statistics as S
def split(arm,alloc='front',skip_pred=True,P0mode='first_agent'):
    T=load(arm); pi,pc,po=[x/1e6 for x in prices(arm)]
    b=dict(pre_cr=0,pre_fr=0,his_cr=0,his_fr=0,out=0,pred=0); ptok=dict(pre=0,tot=0)
    for t,v in T.items():
        agent=[r for r in v if r['ntools']>0]; pred=[r for r in v if r['ntools']==0]
        for r in pred: b['pred']+=(r['P']-r['C'])*pi+r['C']*pc+r['O']*po
        if skip_pred: seq=agent
        else: seq=v
        P0=seq[0]['P']
        for r in seq:
            p=min(P0,r['P']); h=r['P']-p
            if alloc=='front':
                cp=min(r['C'],p); ch=r['C']-cp
            elif alloc=='prorata':
                cp=r['C']*p/r['P']; ch=r['C']-cp
            elif alloc=='back':   # cache fills from the back (extreme: history cached first)
                ch=min(r['C'],h); cp=r['C']-ch
            fp=p-cp; fh=h-ch
            b['pre_cr']+=cp*pc;b['pre_fr']+=fp*pi;b['his_cr']+=ch*pc;b['his_fr']+=fh*pi;b['out']+=r['O']*po
            ptok['pre']+=p;ptok['tot']+=r['P']
    return b,ptok
if __name__=='__main__':
    for alloc in ['front','prorata','back']:
        for arm in ['mm_all','mm_sub','glm_all','glm_sub']:
            b,pt=split(arm,alloc); tot=sum(b.values())
            print(alloc,arm,'tot %.4f'%tot,' '.join('%s %.0f%%'%(k,100*v/tot) for k,v in b.items()),'| prefix tok share (agent reqs) %.1f%%'%(100*pt['pre']/pt['tot']))
    # naive: first request incl predictor
    for arm in ['mm_sub','glm_sub']:
        b,pt=split(arm,'front',skip_pred=False); tot=sum(b.values())
        print('NAIVE first-request',arm,'tot %.4f'%tot,' '.join('%s %.0f%%'%(k,100*v/tot) for k,v in b.items()),'prefix share %.1f%%'%(100*pt['pre']/pt['tot']))
