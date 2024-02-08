# Intro to ML: Lecture 3 Recap

## Two sets of $D$-dimensional points $\boldsymbol{X_1}$ and $\boldsymbol{X_2}$ are linearly separable

1. (*) If there exist $\boldsymbol{w}$, such that $\boldsymbol{x}^T\boldsymbol{w} > 0$ for each $\boldsymbol{x} \in \boldsymbol{X}_1$ and $\boldsymbol{x}^T\boldsymbol{w} < 0$ for each $\boldsymbol{x} \in \boldsymbol{X}_2$.
2. If there exist $\boldsymbol{w}$ such that all points from $\boldsymbol{X}_1$ and $\boldsymbol{X}_2$ lie on a hyperplane defined by $\boldsymbol{x}^T\boldsymbol{w}$.
3. If there exist a projection matrix $\boldsymbol{W}$ such that for each $\boldsymbol{x} \in \boldsymbol{X}_1$ there exists $\bar{\boldsymbol{x}} \in \boldsymbol{X}_2$, such that $\boldsymbol{x}\boldsymbol{W} = \bar{\boldsymbol{x}}$
4. If linear regressions fit for $\boldsymbol{X}_1$ and $\boldsymbol{X}_2$ have the same parameters.


## Select a false claim about Bernoulli distribution.

1. Bernoulli distribution has two outcomes with probabilities $\varphi$ and $1 - \varphi$.
2. $P(x) = \varphi^x(1 - \varphi)^{1-x}$.
3. (*) The entropy of Bernoulli distribution can never be zero.
4. Bernoulli distribution has zero entropy if $\varphi = 0$ or $\varphi = 1$.


## Entropy of a discrete random variable $X$

1. Is only defined if all outcomes have non-zero probability.
2. Can be both positive and negative.
3. (*) Is an expectation of $-\log P(x)$.
4. Is a real number between zero and $e$ (if we use natural logarithm).


## KL divergence of distributions $P$ and $Q$

1. Is a difference between two cross-entropies: $H(P, Q) - H(Q, P)$.
2. (*) Has the following interpretation: It says how many extra nats we need if we encoded messages from distribution $P$ using an encoding for distribution $Q$ compared to the optimum encoding.
3. Can be both positive and negative because of Gibbs inequality.
4. Is metric function because it is reflexive, symmetric and follows the triangular inequality.


## Maximum likelihood estimation implies

1. Finding the most probable training data for given parameters.
2. Maximizing the entropy of the training data, such that the model does make unnecessary assumptions about the data.
3. Classification with logistic regression.
4. (*) Finding parameters that maximize the probability of the training data given the model.


## Select a false statement about logistic regression.

1. It models binary classification using Bernoulli distribution.
2. $P(C_1|\boldsymbol{x},\boldsymbol{w}) = \frac{1}{1 - \exp(-\boldsymbol{x}^\boldsymbol{w})}$, $P(C_0 | \boldsymbol{x}, \boldsymbol{w}) = 1 - P(C_1| \boldsymbol{x}, \boldsymbol{w})$.
3. With fixed parameters $\boldsymbol{w}$, it leads to the same classification as the perceptron model.
4. (*) It is a results of applying the maximum likelihood estimation when we assume that the errors are normally distributed.


