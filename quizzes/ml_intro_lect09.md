# Intro to ML: Lecture 9 Recap (Decision Trees, Random Forests)

## Select a **false** statement about model ensembling.

1. It works best for models with uncorrelated errors.
2. It suffers from **diminishing returns**, i.e., adding more and more models brings less and less improvement.
3. It is a form of regularization because it reduces the **representational capacity** of the model.
4. It is **averaging the predictions** of multiple models.
5. (X) For classifiers with uncorrelated errors, the expected **gain** from ensembling **grows linearly** with the number of models.


## What is knowledge distillation?

1. (X) Training a model to predict the output of a bigger model or an ensemble of models.
2. Searching for a small model by gradually decreasing the number of parameters.
3. Training a model with a smoothed target distribution, sometimes called label smoothing.
4. Training a model with a regularizer that penalizes the number of parameters.

## Select a **false stament** about training a decision tree.

1. We start with a single node.
2. The training data are stored in the tree leaves.
3. At each step, we split the data in the current node into two subsets based on a criterion.
4. (X) The goal of the training is to minimize the number of splits.


## When building a decision tree for regression, we use the following criterion to split the data $I_\mathcal{T}$ in a node $\mathcal{T}$:

1. $\operatorname{Var}(I_\mathcal{T})$
2. (X) $|I_\mathcal{T}| \operatorname{Var}(I_\mathcal{T})$
3. $\operatorname{Var}(I_\mathcal{T}) / |I_\mathcal{T}|$
4. $\sum_{i \in I_\mathcal{T}} t_i^2$


## The relationship between the loss function and the splitting criterion is:

1. The loss function is the splitting criterion.
2. (X) The splitting criterion is the lower bound of the loss function given the tree structure.
3. Splitting criterion is the derivative of the loss function.
4. The loss function is the derivative of the splitting criterion.
5. There is no relationship, they are independent hyperparameters.


## Optimizing negative log-likelihood of the correct class in a categorical distribution leads to

1. (X) The entropy criterion $-|I_\mathcal{T}|\sum_{\text{classes }k}p_k \log p_k$.
2. The cross-entropy criterion $-|I_\mathcal{T}|\sum_{\text{classes }k}p_k \log q_k$, where $q$ is an empirical distribution over the whole training set.
3. The Gini impurity criterion $|I_\mathcal{T}|\sum_{\text{classes }k}p_k (1-p_k)$.
4. An NP-hard problem, so we only predict a single class, instead of a probability distribution.


## Select a **false statement** about random forests.

1. We use bagging to sample the training data independently for each tree in the forest.
2. When splitting a node, we use a random subset of features.
3. We use the same splitting criterion as for decision trees.
4. The final prediction is the average of the predictions of all trees.
5. (X) Random forests are more prone to overfitting than decision trees.


## The difference between random forests and gradient boosted decision trees is:

1. Random forests use a single decision tree, while gradient boosted decision trees use multiple decision trees.
2. (X) Random forests make independent predictions, while gradient boosted decision trees make predictions sequentially.
3. Random forests use a single loss function, while gradient boosted decision trees use multiple loss functions.
4. Random forests use random splits, while gradient boosted decision trees use deterministic splits.


