# AIR-003 experimental protocol
Educational reproduction, not preregistration or novel research. Fixed before execution: seeds 11, 22, 33; independent synthetic samples. Report all configurations. Rates are Monte Carlo estimates, not measurements on real models or patients.
- EXP-001: summary statistics and normal CDF versus NumPy/SciPy, maximum absolute discrepancy.
- EXP-002: standardized exponential sample means, n=5,30,100; 4000 trials; descriptive KS distance to normal.
- EXP-003: normal samples n=5,20,50; 3000 trials; 95% Student-t versus plug-in normal interval coverage with unknown population SD.
- EXP-004: n=20, standardized effects 0,.3,.6; 4000 trials; two-sided t rejection rates versus noncentral-t power.
- EXP-005: exponential mean, n=10,40; 250 trials, 499 resamples per sample; percentile bootstrap versus t-interval coverage.
- EXP-006: independent normal paired differences, n=20, effects 0,.5; 300 trials, 499 Monte Carlo sign flips; compare with paired t rejection rate.
- EXP-007: n=10,30,100, effects .2,.5,.8; 4000 trials; simulation versus analytic t power.
- EXP-008: 4000 families of 20 independent uniform true-null p-values; probability of any false rejection with unadjusted, Bonferroni, Holm and BH methods at .05. Under global null BH FDR equals FWER; no mixed-null or dependence claims.
Expect generally improved normal approximation as n grows, near-nominal t coverage under normality, higher power with larger effect/sample size, and lower global-null false rejection with adjustments. Bootstrap and t may under-cover skewed samples. Use across-seed sample SD, not confidence intervals. Compare identical runs at absolute tolerance 1e-10, relative tolerance zero. No external datasets or paid services.
