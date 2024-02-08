# Intro to ML: Lecture 10 Recap (Gradient Boosted Decision Trees)

## One step in second-order minimization of function $f(x)$ is

1. $\alpha f'(x)$ where $\alpha$ is the learning rate, which is a hyperparameter.
2. $\alpha f''(x)$ where $\alpha$ is the learning rate, which is not a hyperparameter.
3. (*) $-f'(x) / f''(x)$
4. $f''(x) / f'(x)$


## When we apply the Taylor on the loss function $\ell (t_i, y^{(t-1)}(\boldsymbol{x}_i) + y_t(\boldsymbol x_i))$ we get (the $'$ denotes taking derivative by $y^{(t-1)}(\boldsymbol{x}_i)$)

1. (*) $\ell (t_i, y^{(t-1)}(\boldsymbol{x}_i)) + \ell'(t_i, y^{(t-1)}(\boldsymbol{x}_i)) y_t(\boldsymbol x_i) + \frac{1}{2} \ell''(t_i, y^{(t-1)}(\boldsymbol{x}_i)) y_t(\boldsymbol x_i)^2$
2. $\ell (t_i, y^{(t-1)}(\boldsymbol{x}_i)) + \ell'(t_i, y^{(t-1)}(\boldsymbol{x}_i)) y_t(\boldsymbol x_i) + \ell''(t_i, y^{(t-1)}(\boldsymbol{x}_i)) y_t(\boldsymbol x_i)$
3. $\ell (t_i, y^{(t-1)}(\boldsymbol{x}_i)) + \ell'(t_i, y^{(t-1)}(\boldsymbol{x}_i)) + \frac{1}{2} \ell''(t_i, y^{(t-1)}(\boldsymbol{x}_i))^2$
4. $\ell (t_i, y^{(t-1)}(\boldsymbol{x}_i)) + 2\ell'(t_i, y^{(t-1)}(\boldsymbol{x}_i)) \ell''(t_i, y^{(t-1)}(\boldsymbol{x}_i)) y_t(\boldsymbol x_i)$


## The splitting criterion in gradient boosted decision trees is

1. the sum of squared errors.
2. (*) a negative fraction of the first and second derivative of the loss function (when neglecting the regularization term).
3. a negative fraction of the first derivative of the loss function (when neglecting the regularization term).
4. the sum of the first three terms in the Taylor expansion of the loss function.


## Gradient boosted decision trees for binary classification

1. (*) first predict the logit and then applies the sigmoid function.
2. predict the probability in the first tree and real-valued correction in the following trees.
3. are different from gradient boosted decision trees for regression. We still use mean squared error, the splitting criterion becomes the Gini index.
4. are computationally more efficient than gradient boosted decision trees for regression.


## Gradient boosted decision trees for multi-class classification

1. are not possible, each tree can only predict a binary class.
2. (*) use a separate sequence of trees for each class logit, which are then normalized to probabilities using softmax.
3. use a single sequence of trees, where node predict a categorical distribution over classes.
4. use sequence of tree sequences: each set of tree does one-vs-all classification.


## Select a **false** statement about choosing a suitable model for a task.

1. Gradient boosted decision trees are well suited for tabular data.
2. (*) Gradient boosted decision trees are well suited for image data because each tree can capture a different combination of pixel values.
3. Multilayer perceptrons are well suited for high-dimensional data because fully connected layers can capture complex interactions between features.
4. Ensembling can almost always improve the performance of a single model.


