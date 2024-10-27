# Intro to ML: Lecture 2 Recap (Regularization, Hyperparameters, SGD)

## What is regularization?

1. Increasing model capacity, so it better fits the training data.
2. Data preprocessing that makes sure that the training data matrix $\boldsymbol{X}$ is regular.
3. A different name for preventing underfitting.
4. (X) Decreasing model capacity to avoid overfitting.


## Hyperparameters

1. are an order of magnitude bigger than the standard parameters.
2. (X) need to be decided before optimization on training data.
3. are a results of training on validation data.
4. are the best possible set of parameters that we can reach during training.


## Select a false statement about $L^2$-regularization with linear regression.

1. (X) The higher the $\lambda$ value, the lower the training error.
2. We add $\frac{\lambda}{2}||w||^2$ to the error function.
3. We add $\frac{\lambda}{2} \sum_j w_j^2$ to the error function.
4. Linear regression with $L^2$-regularization is sometimes called the Ridge regression.


## What is a correct equation for variance of a discrete random variable?

1. (X) $\operatorname{Var}(x) = \mathbb{E}[x^2] - (\mathbb{E}[x])^2$
2. $\operatorname{Var}(x) = \left(\mathbb{E}[x^2]\right)^2$
3. $\operatorname{Var}(x) = \mathbb{E}\left[ x - \mathbb{E}[x^2] \right]$
4. $\operatorname{Var}(x) = \mathbb{E}\left[ 2x \mathbb{E}[x] \right]$


## What holds about comparing exact solution and SGD solution of linear regression:

1. Unlike exact solution, SGD is not guaranteed to find an optimal solution on the training data.
2. (X) With SGD, we can select a good solution on validation data when doing early stopping.
3. We cannot compute the exact solution for polynomial features. In that case, we must use SGD.
4. The exact solution fails when using $L^2$-regularization because $\boldsymbol{X^T X + \lambda\boldsymbol{I}}$ is always singular, so we have to use SGD.


## SGD is guaranteed to converge.

1. Only if the sum of learning rates $\alpha_i$ is finite but monotonically decreasing.
2. Only for convex functions. Otherwise, it oscillates between multiple local optima.
3. (X) To a local optimum of a continuous function if $\sum_i \alpha_i$ is infinite but $\sum_i \alpha_i^2$ is finite.
4. To the global optimum of a convex function regardless of the learning rate.


## Select an incorrect statement about learning curves.

1. Learning curves show the values of the train and validation errors during the SGD training.
2. (X) The train and validation curve can never cross. If they do, there is an implementation bug.
3. They can be used to visually check if the model is overfitting.
4. They typically do not show the error on the test data. We should not choose the model based on test data, but use the validation data instead.


