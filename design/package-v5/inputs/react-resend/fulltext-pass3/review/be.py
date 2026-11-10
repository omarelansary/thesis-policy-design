def costs(N,M,c):
    un=sum(1+c*(t-1) for t in range(1,N+1))
    ma=sum((1+c*(t-1)) if t<=M else M for t in range(1,N+1))
    return un,ma
for c in (0.05,0.1,0.186,0.2,0.5,1.0):
    for M in (3,10):
        be=None
        for N in range(1,2000):
            un,ma=costs(N,M,c)
            if ma<un: be=N;break
        # cumulative
        print('c=%.3f M=%d  first N masked<unmasked: %s ; doc M/c=%.0f ; (2-c)M/c=%.0f'%(c,M,be,M/c,(2-c)*M/c))
