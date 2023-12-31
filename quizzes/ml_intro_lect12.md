# Intro to ML: Lecture 12 Recap (Hypotheses Testing)

## 1. The $p$ in statistical hypothesis testing is the probability of:

1. The null hypothesis being true.
2. The alternative hypothesis being true.
3. (*) The data being as extreme as the observed data, given that the null hypothesis is true.
4. The observed data given that the null hypothesis is true.


## 2. The error that the hypothesis testing framework is mostly concerned with is:

1. (*) False positives: Falsely rejecting the null hypothesis.
2. False negatives: Falsely accepting the null hypothesis.
3. Both of the above.


## 3. Minimizing Family-Wise Error Rate (FWER) means:

1. (*) Minimizing the probability of making at least one false positive.
2. Randomizing the data to avoid random false positives.
3. Rephrasing the hypothesis to avoid false positives.
4. Changing the significance level based on the $p$-value of previous tests.


## 4. Bootrap resampling is a method for:

1. Estimating the probability of making a false positive.
2. Non-parametric hypothesis testing with $t$-statistics.
3. (*) Estimating a confidence interval for a statistic.
4. For simulating having multiple models with different random seeds.


## 5. The Paired Bootstrap Test

1. (*) Directly estimates the probability of one model scoring higher than another.
2. Means comparing estimated confidence intervals for the two models for overlap.
3. Is a non-parameteric numerical approximation of the $p$-value.
4. Is in fact a two-sample test and is only called "paired" because it uses the same data for both models.


## 6. The Permutation Test

1. Is not a valid test because it does not estimate the $p$-value.
2. (*) Works with the null hypothesis that the two models are the same.
3. Uses bootstrapping to estimate the $p$-value.
4. Is a parametric test that assumes the data is normally distributed. The permutations we use, the closer we are to the normal distribution.


