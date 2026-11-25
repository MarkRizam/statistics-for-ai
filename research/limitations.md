# Scope and limitations

- All data are synthetic; three seeds are descriptive, not a representative sample of tasks or populations.
- Normal-model inference assumes independent observations; paired inference assumes independent pairs. Chi-square is goodness-of-fit with fixed expected counts and suitable asymptotic counts (no fitted parameters). No clustered, repeated-measures or weighted samples.
- Percentile bootstrap may under-cover skewed data and small samples; only iid resampling. Sign-flip requires symmetry/exchangeability under the null; Monte Carlo p-values are discrete.
- Sample size is for a two-sided one-sample/paired normal-model t test with standardized difference, not a general study design. Very extreme numerical inputs remain outside validated scope.
- Holm and Bonferroni control familywise error; BH controls FDR under independence/appropriate positive dependence. The global-null experiment does not evaluate mixed-null or correlated tests.
- No p-value is a probability that a hypothesis is true. Statistical significance is not practical importance.
- No external AI data, human participants, clinical outcomes, Docker verification, linting or runtime/memory comparison. Not peer-reviewed or novel research.
