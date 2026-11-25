"""AIR-003 V1.1 numerical edge cases."""
import numpy as np
import pytest
from scipy import stats
from stats_for_ai import (bayes, mean_ci, t_power, chi_square, z_test,
                          t_test, bootstrap_mean_ci, sign_flip_test)


def test_near_one_confidence():
    c=np.nextafter(1.,0.)
    lo,hi=mean_ci([1.,2.,3.],c)
    half=stats.t.isf((1-c)/2,2)/np.sqrt(3)
    assert np.isfinite([lo,hi]).all()
    assert (lo,hi)==pytest.approx((2-half,2+half))


@pytest.mark.parametrize('p,s,f,expected',[
    (.5,5e-324,5e-324,.5),(.25,5e-324,5e-324,.25),
    (0.,1.,.1,0.),(1.,.1,0.,1.)])
def test_bayes_rare_events(p,s,f,expected):
    assert bayes(p,s,f)==pytest.approx(expected,rel=1e-12,abs=0)


@pytest.mark.parametrize('alpha',[1e-18,1e-22])
def test_small_alpha_power(alpha):
    cutoff=stats.t.isf(alpha/2,19)
    nc=.5*np.sqrt(20)
    expected=stats.nct.sf(cutoff,19,nc)+stats.nct.sf(cutoff,19,-nc)
    assert expected>0
    assert t_power(20,.5,alpha)==pytest.approx(expected,rel=1e-12,abs=0)


@pytest.mark.parametrize('o,e',[([0,0],[1e-14,1e-14]),([1e-14,1e-14],[2e-14,2e-14])])
def test_chi_square_invalid_small_totals(o,e):
    with pytest.raises(ValueError): chi_square(o,e)


@pytest.mark.parametrize('fn',[
    lambda:z_test([1e308,1e308]),
    lambda:z_test([1.],sigma=5e-324),
    lambda:t_test([1.,2.],mu=1e308),
    lambda:chi_square([1e308,1e308],[1e308,1e308]),
    lambda:bootstrap_mean_ci([1e308,1e308],resamples=10),
    lambda:sign_flip_test([1e308,1e308],resamples=10),
])
def test_nonfinite_arithmetic_rejected(fn):
    with pytest.raises(FloatingPointError): fn()
