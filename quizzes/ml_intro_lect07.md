# Intro to ML: Lecture 7 Recap (k Nearest Neighbors, Naive Bayes)

## Select a false statement about the $k$ nearest neighbors classifier.

1. It is a non-parametric method.
2. At inference time, it retrieves the $k$ nearest neighbors of the test point from the training set.
3. (X) It is a parametric method because we need to learn the $k$ parameter.
4. Typically, requires an efficient data structure to avoid a linear search.


## A correct formulat for the Bayes theorem is:

1. $P(y|x) = \frac{P(x|y)P(y)}{P(x|y)P(y) + P(x|\neg y)P(y)}$
2. (X) $P(y|x) = \frac{P(x|y)P(y)}{P(x)}$
3. $P(y|x) = \frac{P(x,y)}{P(x)}$
4. $P(y|x) = \arg\max_y P(x|y)P(y)$


## The Bayesian interpretation of the $L^2$ regularization is that

1. (X) it corresponds to a Gaussian prior on the weights.
2. it corresponds to assuming nothing about the weights, i.e., no Baysian prior.
3. it maximizes the entropy of the posterior distribution.
4. the parameter $\lambda$ is the prior probability of each class.


## The naive assumption in the naive Bayes classifier is that

1. (X) the features are conditionally independent given the class.
2. all features are normally distributed with zero mean.
3. the features are independent of the class, i.e., $P(\boldsymbol{x} \mid C_k) = P(\boldsymbol{x})$
4. the features can be modeled with a Gaussian, Bernoulli, or multinomial distribution.


## In Guassian Naive Bayes, the distribution feature $d$ given class $k$ is modeled as

1. Normal distribution with zero mean and unit variance.
2. Squared distance to the mean of the class.
3. Normal distribution with mean $\frac{1}{|\mathcal{C_k}|}\sum_i x_i,d \cdot \mathbb{1}[\boldsymbol x_i \in \mathcal{C_k}]$ and unit variance.
4. (X) Normal distribution with mean $\frac{1}{|\mathcal{C_k}|}\sum_i x_i,d \cdot \mathbb{1}[\boldsymbol x_i \in \mathcal{C_k}]$ and corresponding variance.


## Select a true statement about the Bernoulli Naive Bayes classifier.

1. It assumes features come from a multinomial distribution.
2. A binary feature only contributes to the classification if it has value 1.
3. (X) It is a special case of a linear model.
4. It can only be used for binary classification.


