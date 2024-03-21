# Large Language Models: Lecture 3 Recap



## What is the objective for training generative LLMs?

1. Predicting the right token on a masked position inside a target sequence.
2. Predicting the right sequence of tokens given a prefix.
3. (X) Predicting the right token that follows a given prefix.


<!-- # Which of the following is the formula for the cross-entropy loss? -->

<!-- 1. $\max(0, 1 - \hat{y} \cdot y)$ -->
<!-- 2. $(y - \hat{y}^2)$ -->
<!-- 3. (X) $- \frac{1}{|\mathcal{D}|} \sum_{(x,y) \in \mathcal{D}} \log p_{\theta}(y|x)$ -->


## Which of the following is NOT an effect of applying the objective used for training generative LLMs?

1. (X) Increasing the cross-entropy of a one-hot distribution of the correct token
   and the distribution predicted by the model.
2. Increasing the probability of the correct item on the target position.
3. Decreasing the probabilities of incorrect tokens on the target position.
4. Decreasing the cross-entropy of a one-hot distribution of the correct token
   and the distribution predicted by the model.


## Why do training optimizers use momentum?

1. To prevent too high learning rates.
2. To avoid overfitting.
3. (X) To speed up the convergence.
4. Because it guarantees convergence into the global optimum.


## What do we mean by instruction tuning?

1. Instead of using training data, we imperatively tell the model how to update the weights using a dynamic programming algorithm.
2. (X) Formatting the task-specific data as instructions in natural language and using those to further train a pretrained model..
3. Adding sentences that resemble instructions into the training data of the pretrained model.
4. Using human feedback in combination with the reinforcement learning objective.


## What do we use RLHF for?

1. (X) To adapt the model responses to match human preference.
2. To train the model to imitate humans.
3. To prevent overfitting.
4. To decrease the model bias.
