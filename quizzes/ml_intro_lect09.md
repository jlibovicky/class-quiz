# Intro to ML: Lecture 9 Recap (Decision Trees, Random Forests)

## 1. Select a **false stament** about training a decision tree.

1. We start with a single node.
2. The training data are stored in the tree leaves.
3. At each step, we split the data in the current node into two subsets based on a criterion.
4. (*) The goal of the training is to minimize the number of splits.


## 2. When building a decision tree for regression, we use the following criterion to split the data $I_\mathcal{T}$ in a node $\mathcal{T}$:

1. $\operatorname{Var}(I_\mathcal{T})$
2. (*) $|I_\mathcal{T}| \operatorname{Var}(I_\mathcal{T})$
3. $\operatorname{Var}(I_\mathcal{T}) / |I_\mathcal{T}|$
4. $\sum_{i \in I_\mathcal{T}} t_i^2$


## 3. The relationship between the loss function and the splitting criterion is:

1. The loss function is the splitting criterion.
2. (*) The splitting criterion is the lower bound of the loss function given the tree structure.
3. Splitting criterion is the derivative of the loss function.
4. The loss function is the derivative of the splitting criterion.
5. There is no relationship, they are independent hyperparameters.


## 4. Optimizing negative log-likelihood of the correct class in a categorical distribution leads to

1. (*) The entropy criterion $-|I_\mathcal{T}|\sum_{\text{classes }k}p_k \log p_k$.
2. The cross-entropy criterion $-|I_\mathcal{T}|\sum_{\text{classes }k}p_k \log q_k$, where $q$ is an empirical distribution over the whole training set.
3. The Gini impurity criterion $|I_\mathcal{T}|\sum_{\text{classes }k}p_k (1-p_k)$.
4. An NP-hard problem, so we only predict a single class, instead of a probability distribution.


## 5. Select a **false statement** about random forests.

1. We use bagging to sample the training data independently for each tree in the forest.
2. When splitting a node, we use a random subset of features.
3. We use the same splitting criterion as for decision trees.
4. The final prediction is the average of the predictions of all trees.
5. (*) Random forests are more prone to overfitting than decision trees.


## 6. The difference between random forests and gradient boosted decision trees is:

1. Random forests use a single decision tree, while gradient boosted decision trees use multiple decision trees.
2. (*) Random forests make independent predictions, while gradient boosted decision trees make predictions sequentially.
3. Random forests use a single loss function, while gradient boosted decision trees use multiple loss functions.
4. Random forests use random splits, while gradient boosted decision trees use deterministic splits.


