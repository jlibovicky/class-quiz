# Intro to ML: Lecture 8 Recap (Correlation, Model Combiation)

## What is an **incorrect** equation for covariance?

1. $\operatorname{Cov}(\mathbf{x}, \mathbf{y}) = \mathbb{E}\left[ (\mathbf{x} - \mathbb{E}[\mathbf{x}])(\mathbf{y} - \mathbb{E}[\mathbf{y}]) \right]$
2. $\operatorname{Cov}(\mathbf{x}, \mathbf{y}) = \mathbb{E}[\mathbf{x}\mathbf{y}] - \mathbb{E}[\mathbf{x}]\mathbb{E}[\mathbf{y}]$
3. $\operatorname{Cov}(\mathbf{x}, \mathbf{y}) = \sum_{x,y} P(x, y)(x - \mathbb{E}[\mathbf{x}]) (y - \mathbb{E}[\mathbf{y}])$
4. (X) $\operatorname{Cov}(\mathbf{x}, \mathbf{y}) = \mathbb{E}\left[\log \frac{P(x, y))}{P(x)P(y)}\right]$


## What is the correct equation for Pearson correlation?

1. $\rho = \frac{\operatorname{Cov}(\mathbf{x}, \mathbf{y})^2}{\operatorname{Var}(\mathbf{x})\operatorname{Var}(\mathbf{y})}$
2. (X) $\rho = \frac{\operatorname{Cov}(\mathbf{x}, \mathbf{y})}{\sqrt{\operatorname{Var}(\mathbf{x})}\sqrt{\operatorname{Var}(\mathbf{y})}}$
3. $\rho = \operatorname{Cov}(\mathbf{x}, \mathbf{y}) - \operatorname{Var}(\mathbf{x})\operatorname{Var}(\mathbf{y})$
4. $\rho = \sqrt{\frac{\operatorname{Cov}(\mathbf{x}, \mathbf{y})}{\operatorname{Var}(\mathbf{x})\operatorname{Var}(\mathbf{y})}}$


## What is the relation between Spearman and Pearson correlation?

1. They are the same, but in different scale.
2. (X) Spearman correlation is Pearson correlation on the ranks of the data.
3. Pearson correlation quantifies the linear relationship between two variables, while Spearman correlation quantifies quadratic relationship.
4. Pearson correlation is ideal value, whereas Spearman correlation is an estimate from the data.


## What is the difference between Spearman correlation $\rho$ and Kendal's $\tau$?

1. $\rho$ is inversely proportional to $\tau$.
2. (X) They are different metrics for quantifying rank correlation.
3. They are equivalent up to a constant.
4. Spearman correlation is considered obsolete and in newer papers replaced by Kendal's $\tau$.

## Cohen's $\kappa$ quantifies

1. normalized Spearman correlation between ranking by two annotators.
2. (X) the probability of the actual agreement between two annotators compared to a chance agreement.
3. probability of two annotators agreeing on a label given the Pearson correlation of their annotations.
4. the upper bound of a classifier accuracy trained on data from the given annotation.


## What is mean reciprocal rank (MRR) used for?

1. Evaluation of inter-annotator agreement for regression tasks.
2. (X) Evaluation of ranking tasks.
3. Evaluation of multilabel classification with very imbalanced classes.
4. Assessing feature importance of linear models.