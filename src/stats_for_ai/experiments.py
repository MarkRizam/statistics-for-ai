"""Fixed synthetic experiment runner."""
import json
import platform
from pathlib import Path
import numpy as np
import scipy
from scipy import stats
from .core import describe,covariance,normal_cdf,bootstrap_mean_ci,mean_ci,sign_flip_test,t_power,adjust_pvalues

SEEDS=(11,22,33)


def run():
    rows=[]
    def add(exp,seed,config,metric,ours,reference,reference_kind,trials):
        rows.append(dict(experiment=exp,seed=seed,configuration=config,metric=metric,ours=float(ours),reference=float(reference),reference_kind=reference_kind,trials=trials))
    for seed in SEEDS:
        rng=np.random.default_rng(seed); x,y=rng.normal(size=(2,100)); d=describe(x)
        errors=[abs(d['mean']-x.mean()),abs(d['sample_variance']-x.var(ddof=1)),abs(covariance(x,y)-np.cov(x,y)[0,1]),abs(normal_cdf(1.3)-stats.norm.cdf(1.3))]
        add('EXP-001',seed,'summary and CDF','max absolute discrepancy',max(errors),0,'analytic ideal',100)
        for n in (5,30,100):
            z=(rng.exponential(size=(4000,n)).mean(1)-1)*np.sqrt(n)
            add('EXP-002',seed,f'n={n}','KS distance to normal',stats.kstest(z,'norm').statistic,0,'analytic ideal',4000)
        for n in (5,20,50):
            x=rng.normal(size=(3000,n)); means=x.mean(1); se=x.std(1,ddof=1)/np.sqrt(n)
            add('EXP-003',seed,f'n={n}','95% interval coverage',np.mean(np.abs(means)<=stats.t.ppf(.975,n-1)*se),np.mean(np.abs(means)<=stats.norm.ppf(.975)*se),'plug-in normal interval',3000)
        for effect in (0,.3,.6):
            n=20; x=rng.normal(loc=effect,size=(4000,n)); t=x.mean(1)/(x.std(1,ddof=1)/np.sqrt(n))
            add('EXP-004',seed,f'd={effect:g}','rejection rate',np.mean(np.abs(t)>stats.t.ppf(.975,n-1)),t_power(n,effect),'noncentral-t analytic power',4000)
        for n in (10,40):
            hit_b=hit_t=0
            for i,x in enumerate(rng.exponential(size=(250,n))):
                lo,hi=bootstrap_mean_ci(x,resamples=499,seed=seed*10000+i); hit_b+=lo<=1<=hi
                lo,hi=mean_ci(x); hit_t+=lo<=1<=hi
            add('EXP-005',seed,f'n={n}','95% interval coverage',hit_b/250,hit_t/250,'Student-t interval',250)
        for effect in (0,.5):
            n=20; x=rng.normal(loc=effect,size=(300,n)); t=x.mean(1)/(x.std(1,ddof=1)/np.sqrt(n))
            p=np.array([sign_flip_test(v,499,seed=seed*10000+i) for i,v in enumerate(x)])
            add('EXP-006',seed,f'd={effect:g}','rejection rate',np.mean(p<=.05),np.mean(np.abs(t)>stats.t.ppf(.975,n-1)),'paired t test',300)
        for effect in (.2,.5,.8):
            for n in (10,30,100):
                x=rng.normal(loc=effect,size=(4000,n)); t=x.mean(1)/(x.std(1,ddof=1)/np.sqrt(n))
                add('EXP-007',seed,f'd={effect:g}, n={n}','rejection rate',np.mean(np.abs(t)>stats.t.ppf(.975,n-1)),t_power(n,effect),'noncentral-t analytic power',4000)
        p=rng.uniform(size=(4000,20)); alpha=.05
        add('EXP-008',seed,'unadjusted','familywise false rejection rate',np.mean((p<=alpha).any(1)),1-(1-alpha)**20,'independent global-null theory',4000)
        for method in ('bonferroni','holm','bh'):
            adjusted=np.array([adjust_pvalues(row,method) for row in p]); target=alpha if method=='bh' else 1-(1-alpha/20)**20
            add('EXP-008',seed,method,'familywise false rejection rate',np.mean((adjusted<=alpha).any(1)),target,'independent global-null theory',4000)
    return rows


def compare(a,b):
    assert len(a)==len(b)==81
    for x,y in zip(a,b):
        assert x.keys()==y.keys()
        for k,v in x.items():
            if isinstance(v,float): np.testing.assert_allclose(v,y[k],rtol=0,atol=1e-10)
            else: assert v==y[k],(k,v,y[k])


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    matplotlib.rcParams['svg.fonttype']='none'; matplotlib.rcParams['svg.hashsalt']='AIR-003'
    root=Path.cwd(); (root/'results').mkdir(exist_ok=True); (root/'figures').mkdir(exist_ok=True)
    a,b=run(),run(); compare(a,b); summary=[]
    for exp in sorted({r['experiment'] for r in a}):
        rows=[r for r in a if r['experiment']==exp]; configs=list(dict.fromkeys(r['configuration'] for r in rows)); group=[]
        for c in configs:
            records=[r for r in rows if r['configuration']==c]
            row=dict(experiment=exp,configuration=c,metric=records[0]['metric'],reference_kind=records[0]['reference_kind'],n=len(records),trials_per_seed=records[0]['trials'])
            for k in ('ours','reference'):
                v=[r[k] for r in records]; row[k+'_mean']=float(np.mean(v)); row[k+'_sd']=float(np.std(v,ddof=1))
            group.append(row)
        summary.extend(group)
        fig,ax=plt.subplots(figsize=(9,4.5)); x=np.arange(len(configs))
        for i,k in enumerate(('ours','reference')):
            ax.bar(x+(i-.5)*.35,[r[k+'_mean'] for r in group],.35,yerr=[r[k+'_sd'] for r in group],capsize=3,label='method / simulation' if k=='ours' else 'reference')
        ax.set_xticks(x,configs,rotation=25,ha='right'); ax.set_ylabel(group[0]['metric']); ax.set_title(exp+' — mean and sample SD (3 seeds)'); ax.legend()
        if exp in ('EXP-003','EXP-005'): ax.axhline(.95,linestyle='--',color='gray',linewidth=1)
        if exp=='EXP-008': ax.axhline(.05,linestyle='--',color='gray',linewidth=1)
        fig.tight_layout()
        for ext in ('svg','png'): fig.savefig(root/'figures'/f'{exp}.{ext}')
        plt.close(fig)
    payload=dict(project='AIR-003',seeds=SEEDS,environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,platform=platform.system()),reproducibility=dict(runs=2,atol=1e-10,rtol=0,status='pass'),records=a,summary=summary)
    (root/'results'/'benchmarks.json').write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
    print(f'{len(a)} records; {len(summary)} configurations; 8 experiments; reproducibility PASS')

if __name__=='__main__': main()
