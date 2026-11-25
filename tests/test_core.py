import numpy as np
import pytest
from scipy import stats
from stats_for_ai import *

@pytest.mark.parametrize('seed',[11,22,33])
def test_descriptive(seed):
    x,y=np.random.default_rng(seed).normal(size=(2,30)); d=describe(x)
    assert d['mean']==pytest.approx(x.mean()); assert d['sample_variance']==pytest.approx(x.var(ddof=1))
    assert covariance(x,y)==pytest.approx(np.cov(x,y)[0,1])

@pytest.mark.parametrize('z',[-8,-2,0,2,8])
def test_cdf(z): assert normal_cdf(z)==pytest.approx(stats.norm.cdf(z),rel=1e-12,abs=0)

def test_bayes(): assert bayes(.01,.9,.05)==pytest.approx(.009/.0585)

@pytest.mark.parametrize('seed',[11,22,33])
def test_inference(seed):
    x,y=np.random.default_rng(seed).normal(size=(2,30))
    assert t_test(x)==pytest.approx(tuple(stats.ttest_1samp(x,0)))
    assert paired_t(x,y)==pytest.approx(tuple(stats.ttest_rel(x,y)))
    assert paired_effect(x,y)==pytest.approx((x-y).mean()/(x-y).std(ddof=1))
    assert mean_ci(x)==pytest.approx(stats.t.interval(.95,len(x)-1,loc=x.mean(),scale=stats.sem(x)))
    z,p=z_test(x); assert z==pytest.approx(x.mean()*np.sqrt(len(x))); assert p==pytest.approx(2*stats.norm.sf(abs(z)))

def test_chi_square(): assert chi_square([12,18,20],[15,15,20])==pytest.approx(tuple(stats.chisquare([12,18,20],[15,15,20])))

def test_bootstrap():
    x=[1,2,3,4,5]; a=bootstrap_mean_ci(x,resamples=1000,seed=11); assert a==bootstrap_mean_ci(x,resamples=1000,seed=11); assert a[0]<3<a[1]
    assert bootstrap_mean_ci([2,2],resamples=10)==(2,2)

def test_sign_flip():
    x=[1]*20; p=sign_flip_test(x,499,11); assert p==sign_flip_test(x,499,11); assert 1/500<=p<.05
    assert sign_flip_test([0,0],99)==1

@pytest.mark.parametrize('method',['bh','holm','bonferroni'])
def test_adjustment(method):
    p=np.array([.04,.001,.2,.03]); a=adjust_pvalues(p,method)
    expected={'bh':[.0533333333333333,.004,.2,.0533333333333333],'holm':[.09,.004,.2,.09],'bonferroni':[.16,.004,.8,.12]}
    np.testing.assert_allclose(a,expected[method]); assert np.all(a>=p)
    if method=='bh': np.testing.assert_allclose(a,stats.false_discovery_control(p))

@pytest.mark.parametrize('effect',[.2,.5,.8])
def test_power(effect):
    assert t_power(10,effect)<t_power(100,effect); assert t_power(20,0)==pytest.approx(.05)
    n=required_n(effect); assert t_power(n,effect)>=.8; assert n==2 or t_power(n-1,effect)<.8

@pytest.mark.parametrize('fn',[lambda:describe([1]),lambda:describe([1,np.nan]),lambda:describe(np.array([1+2j,2])),lambda:covariance([1,2],[1,2,3]),lambda:bayes(0,1,0),lambda:bayes(2,.2,.3),lambda:mean_ci([1,2],1),lambda:z_test([1,2],sigma=0),lambda:t_test([1,1]),lambda:paired_t([1,2],[1,2,3]),lambda:paired_effect([1,2],[0,1]),lambda:chi_square([1,2],[1,1]),lambda:chi_square([1,2],[0,3]),lambda:bootstrap_mean_ci([1,2],resamples=0),lambda:sign_flip_test([1,2],True),lambda:t_power(1,.5),lambda:required_n(0),lambda:required_n(.01,max_n=3),lambda:adjust_pvalues([-.1,.2]),lambda:adjust_pvalues([.1],method='other')])
def test_invalid(fn):
    with pytest.raises(ValueError): fn()

@pytest.mark.parametrize('effect',[.2,.5,.8])
def test_power_stable_tails(effect):
    assert t_power(30,effect)==pytest.approx(t_power(30,-effect))
    assert t_power(10000,effect)==pytest.approx(1.)
