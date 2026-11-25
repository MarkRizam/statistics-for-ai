"""Educational statistics; SciPy supplies distribution tails and quantiles."""
import math
import numpy as np
from scipy import stats


def vector(x, minimum=1):
    if np.iscomplexobj(x): raise ValueError('Real samples only')
    a = np.asarray(x, dtype=float)
    if a.ndim != 1 or len(a) < minimum or not np.isfinite(a).all():
        raise ValueError('Expected finite one-dimensional sample')
    return a


def positive_int(n):
    if isinstance(n,(bool,np.bool_)) or not isinstance(n,(int,np.integer)) or n<1:
        raise ValueError('Positive integer required')
    return int(n)


def probability(p, strict=False):
    if np.ndim(p)!=0 or np.iscomplexobj(p) or not np.isfinite(p) or not (0<p<1 if strict else 0<=p<=1):
        raise ValueError('Invalid probability')
    return float(p)


def describe(x):
    x=vector(x,2); mean=float(x.mean()); var=float(np.sum((x-mean)**2)/(len(x)-1))
    if not math.isfinite(mean) or not math.isfinite(var): raise FloatingPointError('Nonfinite summary')
    return dict(n=len(x),mean=mean,sample_variance=var,sample_sd=math.sqrt(var),median=float(np.median(x)))


def covariance(x,y):
    x,y=vector(x,2),vector(y,2)
    if x.shape!=y.shape: raise ValueError('Equal paired lengths required')
    c=float(np.dot(x-x.mean(),y-y.mean())/(len(x)-1))
    if not math.isfinite(c): raise FloatingPointError('Nonfinite covariance')
    return c


def normal_cdf(z):
    if np.ndim(z)!=0 or np.iscomplexobj(z) or not np.isfinite(z): raise ValueError('Finite real z required')
    return math.erfc(-float(z)/math.sqrt(2))/2


def bayes(prior,sensitivity,false_positive):
    p,s,f=map(probability,(prior,sensitivity,false_positive)); m=p*s+(1-p)*f
    if m==0: raise ValueError('Zero probability conditioning event')
    return p*s/m


def mean_ci(x,confidence=.95):
    d=describe(x); c=probability(confidence,True)
    half=stats.t.ppf((1+c)/2,d['n']-1)*d['sample_sd']/math.sqrt(d['n'])
    return d['mean']-half,d['mean']+half


def z_test(x,mu=0.,sigma=1.):
    x=vector(x)
    if not math.isfinite(mu) or not math.isfinite(sigma) or sigma<=0: raise ValueError('Invalid null parameters')
    z=(x.mean()-mu)/(sigma/math.sqrt(len(x)))
    return float(z),float(2*stats.norm.sf(abs(z)))


def t_test(x,mu=0.):
    d=describe(x)
    if not math.isfinite(mu) or d['sample_sd']==0: raise ValueError('Finite null and nonzero SD required')
    t=(d['mean']-mu)/(d['sample_sd']/math.sqrt(d['n']))
    return t,float(2*stats.t.sf(abs(t),d['n']-1))


def paired_t(x,y):
    x,y=vector(x,2),vector(y,2)
    if x.shape!=y.shape: raise ValueError('Equal paired lengths required')
    return t_test(x-y)


def paired_effect(x,y):
    x,y=vector(x,2),vector(y,2)
    if x.shape!=y.shape: raise ValueError('Equal paired lengths required')
    d=describe(x-y)
    if d['sample_sd']==0: raise ValueError('Nonzero difference SD required')
    return d['mean']/d['sample_sd']


def chi_square(observed,expected):
    o,e=vector(observed,2),vector(expected,2)
    if o.shape!=e.shape or (o<0).any() or (e<=0).any() or not np.isclose(o.sum(),e.sum(),rtol=1e-12,atol=1e-12): raise ValueError('Invalid counts or unequal totals')
    v=float(np.sum((o-e)**2/e))
    return v,float(stats.chi2.sf(v,len(o)-1))


def bootstrap_mean_ci(x,confidence=.95,resamples=2000,seed=42):
    x=vector(x,2); c=probability(confidence,True); n=positive_int(resamples)
    rng=np.random.default_rng(seed); means=np.empty(n)
    for i in range(0,n,256):
        k=min(256,n-i); means[i:i+k]=x[rng.integers(len(x),size=(k,len(x)))].mean(1)
    return tuple(map(float,np.quantile(means,[(1-c)/2,(1+c)/2])))


def sign_flip_test(differences,resamples=1999,seed=42):
    """Two-sided Monte Carlo test, requiring independent symmetric null differences."""
    x=vector(differences,2); n=positive_int(resamples); rng=np.random.default_rng(seed)
    observed=abs(x.mean()); exceed=0
    for i in range(0,n,256):
        k=min(256,n-i); null=np.abs((rng.choice([-1.,1.],size=(k,len(x)))*x).mean(1))
        exceed+=int(np.count_nonzero(null>=observed-1e-12*observed))
    return (exceed+1)/(n+1)


def t_power(n,effect,alpha=.05):
    n=positive_int(n); alpha=probability(alpha,True)
    if n<2 or not math.isfinite(effect): raise ValueError('Invalid sample size or effect')
    cutoff=stats.t.ppf(1-alpha/2,n-1); nc=abs(effect)*math.sqrt(n)
    power=float(stats.nct.sf(cutoff,n-1,-nc)+stats.nct.sf(cutoff,n-1,nc))
    if not math.isfinite(power) or not 0<=power<=1+1e-14: raise FloatingPointError("Nonfinite or invalid numerical power")
    return min(power,1.)


def required_n(effect,target=.8,alpha=.05,max_n=10000):
    target=probability(target,True); alpha=probability(alpha,True); max_n=positive_int(max_n)
    if not math.isfinite(effect) or effect==0 or max_n<2: raise ValueError('Invalid effect or search bound')
    lo,hi=2,min(4,max_n)
    while t_power(hi,effect,alpha)<target:
        if hi==max_n: raise ValueError('Target not reached')
        lo,hi=hi+1,min(hi*2,max_n)
    while lo<hi:
        mid=(lo+hi)//2
        if t_power(mid,effect,alpha)>=target: hi=mid
        else: lo=mid+1
    return lo


def adjust_pvalues(pvalues,method='holm'):
    p=vector(pvalues)
    if (p<0).any() or (p>1).any() or method not in ('holm','bh','bonferroni'): raise ValueError('Invalid p-values or method')
    m=len(p)
    if method=='bonferroni': return np.minimum(p*m,1.)
    order=np.argsort(p,kind='stable'); sp=p[order]
    if method=='holm': adjusted=np.maximum.accumulate(sp*np.arange(m,0,-1))
    else: adjusted=np.minimum.accumulate((sp*m/np.arange(1,m+1))[::-1])[::-1]
    result=np.empty(m); result[order]=np.minimum(adjusted,1.)
    return result
