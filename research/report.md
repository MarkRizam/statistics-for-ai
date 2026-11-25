# AIR-003 — Statistics for AI: research report

## Abstract
Eight reproducible educational simulations investigate statistical accuracy, sampling, interval coverage, test rejection rates, resampling, power and multiplicity. Three seeds produce 81 records across 27 configurations. All 44 unit tests and eight teaching notebooks executed locally. These are synthetic demonstrations, not evidence about real AI models or clinical outcomes.

## Methodology
See the fixed [protocol](protocol.md). Samples are independent within each simulation; seeds 11, 22 and 33. NumPy generates data and SciPy supplies distribution tails/quantiles and reference statistics. The implementation computes the statistics, resampling and adjustment algorithms directly. Equal-seed summaries report mean and sample SD; those SDs are not confidence intervals. Trials per seed are counts of simulation replications except EXP-001, which uses 100 paired observations. References include analytic ideals, theoretical rejection rates and competing interval/test procedures; they are not interchangeable performance measures. Two identical runs agreed at absolute tolerance 1e-10, and fresh results matched the committed-candidate snapshot.

## Results
| Experiment | Configuration | Metric | Method / simulation mean ± SD | Reference mean ± SD | Reference type | Trials per seed |
|---|---|---|---:|---:|---|---:|
| EXP-001 | summary and CDF | max absolute discrepancy | 1.21431e-17 ± 4.59e-18 | 0 ± 0 | analytic ideal | 100 |
| EXP-002 | n=5 | KS distance to normal | 0.0656924 ± 0.0023 | 0 ± 0 | analytic ideal | 4000 |
| EXP-002 | n=30 | KS distance to normal | 0.0287878 ± 0.0132 | 0 ± 0 | analytic ideal | 4000 |
| EXP-002 | n=100 | KS distance to normal | 0.0200414 ± 0.00364 | 0 ± 0 | analytic ideal | 4000 |
| EXP-003 | n=5 | 95% interval coverage | 0.950889 ± 0.0015 | 0.877778 ± 0.00517 | plug-in normal interval | 3000 |
| EXP-003 | n=20 | 95% interval coverage | 0.951444 ± 0.00474 | 0.935 ± 0.00603 | plug-in normal interval | 3000 |
| EXP-003 | n=50 | 95% interval coverage | 0.947444 ± 0.00536 | 0.943 ± 0.00437 | plug-in normal interval | 3000 |
| EXP-004 | d=0 | rejection rate | 0.0506667 ± 0.00123 | 0.05 ± 8.5e-18 | noncentral-t analytic power | 4000 |
| EXP-004 | d=0.3 | rejection rate | 0.25125 ± 0.00336 | 0.247089 ± 0 | noncentral-t analytic power | 4000 |
| EXP-004 | d=0.6 | rejection rate | 0.719583 ± 0.00889 | 0.721005 ± 0 | noncentral-t analytic power | 4000 |
| EXP-005 | n=10 | 95% interval coverage | 0.850667 ± 0.026 | 0.886667 ± 0.018 | Student-t interval | 250 |
| EXP-005 | n=40 | 95% interval coverage | 0.929333 ± 0.022 | 0.932 ± 0.0144 | Student-t interval | 250 |
| EXP-006 | d=0 | rejection rate | 0.0377778 ± 0.00509 | 0.0366667 ± 0.00577 | paired t test | 300 |
| EXP-006 | d=0.5 | rejection rate | 0.558889 ± 0.028 | 0.575556 ± 0.0184 | paired t test | 300 |
| EXP-007 | d=0.2, n=10 | rejection rate | 0.09275 ± 0.00607 | 0.0876572 ± 1.7e-17 | noncentral-t analytic power | 4000 |
| EXP-007 | d=0.2, n=30 | rejection rate | 0.188917 ± 0.00851 | 0.185183 ± 0 | noncentral-t analytic power | 4000 |
| EXP-007 | d=0.2, n=100 | rejection rate | 0.503583 ± 0.00138 | 0.508265 ± 0 | noncentral-t analytic power | 4000 |
| EXP-007 | d=0.5, n=10 | rejection rate | 0.294333 ± 0.00439 | 0.293176 ± 0 | noncentral-t analytic power | 4000 |
| EXP-007 | d=0.5, n=30 | rejection rate | 0.75375 ± 0.006 | 0.753965 ± 0 | noncentral-t analytic power | 4000 |
| EXP-007 | d=0.5, n=100 | rejection rate | 0.99825 ± 0.000661 | 0.99861 ± 0 | noncentral-t analytic power | 4000 |
| EXP-007 | d=0.8, n=10 | rejection rate | 0.62225 ± 0.00434 | 0.616233 ± 0 | noncentral-t analytic power | 4000 |
| EXP-007 | d=0.8, n=30 | rejection rate | 0.987833 ± 0.00213 | 0.988475 ± 0 | noncentral-t analytic power | 4000 |
| EXP-007 | d=0.8, n=100 | rejection rate | 1 ± 0 | 1 ± 0 | noncentral-t analytic power | 4000 |
| EXP-008 | unadjusted | familywise false rejection rate | 0.6465 ± 0.0035 | 0.641514 ± 0 | independent global-null theory | 4000 |
| EXP-008 | bonferroni | familywise false rejection rate | 0.0493333 ± 0.00379 | 0.0488301 ± 0 | independent global-null theory | 4000 |
| EXP-008 | holm | familywise false rejection rate | 0.0493333 ± 0.00379 | 0.0488301 ± 0 | independent global-null theory | 4000 |
| EXP-008 | bh | familywise false rejection rate | 0.0499167 ± 0.00391 | 0.05 ± 8.5e-18 | independent global-null theory | 4000 |

## Interpretation
- Standardized exponential sample means approach normality: KS distance fell from 0.06569 at n=5 to 0.02004 at n=100. Finite Monte Carlo sampling adds noise.
- At n=5, normal-data Student-t interval coverage was 95.09%, versus 87.78% for the plug-in normal interval using estimated SD. This does not discredit the z interval with genuinely known population SD.
- At n=20 the null t-test rejection rate was 5.07%; simulated power at standardized effect 0.6 was 71.96%, close to the theoretical 72.10%.
- Percentile-bootstrap coverage on skewed exponential samples was 85.07% at n=10 and 92.93% at n=40; t intervals also under-covered. Bootstrap is not automatically calibrated.
- Sign-flip and paired t rejection rates differed modestly. Only 300 trials per seed and 499 sign flips per trial were used; no claim of equivalent performance.
- At effect 0.5 and n=30, empirical power was 75.38%; theoretical power 75.40%. Under the independent normal one-sample model, two-sided alpha .05 and target power .8, minimum n was 199, 34 and 15 for effects .2, .5 and .8 respectively. These are not clinical study recommendations.
- Under 20 independent true nulls, the unadjusted familywise false rejection rate was 64.65%; Bonferroni/Holm 4.93%; BH 4.99%. BH generally controls FDR, not FWER; the two coincide only under the global null. Mixed-null and dependent-test designs are untested.

## Implementation verification
Initial test execution exposed non-finite noncentral-t CDF values at large noncentrality with the installed SciPy version. The power implementation now uses symmetric survival-function tails and checks finite output; sample-size search brackets the target before binary search. Added three regression cases for large sample size and effect-sign symmetry. Final 44 tests passed, including reference comparisons. Eight clean-source notebooks were executed. Package installation used existing local dependencies (no fresh dependency resolution); hosted verification remains pending. Docker, linting, external data, hardware benchmarks and broader extreme-value stability are not verified.

## Reproduction
Run from the repository root: `python -m pip install -e ".[research]"`, `python -m pytest -q`, `python scripts/verify_committed_results.py`, `python -m stats_for_ai.experiments`, `python scripts/notebooks.py`. Use one numerical-library thread as in CI. Regeneration replaces benchmark/figure outputs; compare committed records first.

## References and limitations
See the [limitations](limitations.md). Reference API: https://docs.scipy.org/doc/scipy/reference/stats.html ; NumPy statistics reference: https://numpy.org/doc/stable/reference/routines.statistics.html . These are source links, not reproduced books. No claim of formal publication, statistical superiority, or external generalization.
