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


## Cohen's $\kappa$ quantifies

1. normalized Spearman correlation between ranking by two annotators.
2. (X) the probability of the actual agreement between two annotators compared to a chance agreement.
3. probability of two annotators agreeing on a label given the Pearson correlation of their annotations.
4. the upper bound of a classifier accuracy trained on data from the given annotation.


## Select a **false** statement about model ensembling.

1. It works best for models with uncorrelated errors.
2. It suffers from diminishing returns, i.e., adding more and more models brings less and less improvement.
3. It is a form of regularization because it reduces the total model capacity.
4. It is averaging the predictions of multiple models.
5. (X) For classifiers with uncorrelated errors, the expected gain from ensembling grows linearly with the number of models.


## What is knowledge distillation?

1. (X) Training a model to predict the output of a bigger model or an ensemble of models.
2. Searching for a small model by gradually decreasing the number of parameters.
3. Training a model with a smoothed target distribution, sometimes called label smoothing.
4. Training a model with a regularizer that penalizes the number of parameters.


