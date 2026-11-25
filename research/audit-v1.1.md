# AIR-003 V1.1 — scientific audit

Baseline: 3842cc53a80d0a928571e2e446a602f50ee431c2. Original hosted [CI run](https://github.com/MarkRizam/statistics-for-ai/actions/runs/45524197043) succeeded. Reviewed core formulas, simulation runner, protocol and committed-result check. Reproduced the defects locally and added 15 regression cases.

## Numerical findings and changes

- Use log-space Bayes normalization to avoid underflow for subnormal nonzero probabilities; retain explicit rejection of impossible conditioning events.
- Use inverse survival quantiles for Student-t intervals and power to avoid rounding upper-tail probabilities to one. A confidence level immediately below one previously returned infinite interval endpoints; very small alpha previously produced zero power spuriously.
- Reject zero observed totals and unequal chi-square totals using relative tolerance without a fixed absolute floor; detect overflow.
- Reject nonfinite z/t statistics and standardized effects; trap overflow in bootstrap and sign-flip calculations rather than reporting NaN intervals or misleading p-values.
- Validate finite power parameters and interval endpoints.

## Executed verification

Local Python 3.13, NumPy 2.3.5 and SciPy 1.17.0: 59/59 tests passed, Python compilation passed, committed-result script passed. Two fresh runs compared with all 81 baseline records using absolute tolerance 1e-10, relative tolerance zero. Maximum baseline-to-fresh absolute numeric difference 6.661338147750939e-16; fresh-to-fresh difference zero. The original benchmark file is unchanged. This is numerical agreement within tolerance, not bitwise equality to the baseline.

## Statistical interpretation

The one-sample t intervals/tests assume independent normal observations for exact finite-sample inference; the z test assumes known population SD and an appropriate normal sampling model. Pearson goodness-of-fit uses fixed expected probabilities and k-1 degrees of freedom, with adequate expected counts required for the asymptotic approximation. Paired t/effect calculations use within-pair differences; sign flips require independent symmetric null differences. Percentile bootstrap is approximate and can under-cover skewed small samples. Power/sample size assumes a one-sample two-sided t model with specified standardized effect and significance level. Holm/Bonferroni control familywise error; BH targets FDR under appropriate dependence assumptions, not general FWER. Under the simulated independent global null, FDR and FWER coincide. Three seed aggregates are descriptive Monte Carlo estimates, not confidence intervals. The simulations do not establish performance on actual AI models or clinical populations.

## Outstanding limitations

Fresh hosted CI is required before merge. Real model evaluations, dependent data, mixed-null experiments, fitted-parameter chi-square tests, broader extreme-value numerical robustness, Docker, linting and performance benchmarks remain unverified. No peer review or novelty claim.

Reproduce: `python -m pytest -q` and `python scripts/verify_committed_results.py`.
