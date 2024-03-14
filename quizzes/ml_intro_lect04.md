# Intro to ML: Lecture 4 Recap

## The weight update in SGD for logistic regression is

1. (X) $(y(\boldsymbol{x}_i, \boldsymbol{w}) - t_i)\boldsymbol{x}_i$
2. $\sigma(\boldsymbol{x}_i^T\boldsymbol{w})\left(1 - \sigma(\boldsymbol{x}_i^T) \right)\boldsymbol{x}_i$
3. $\nabla_\boldsymbol{x} -\log \sigma(\boldsymbol{x}_i^T\boldsymbol{w})^t_i \cdot (1 - \sigma(\boldsymbol{x}_i^T\boldsymbol{w}))^{1 - t_i}$
4. $-t_i\boldsymbol{x}_i$ if $t_i \boldsymbol{x}^T\boldsymbol{w} < 0$


## Linear regression trained with the mean squared error assumes that:

1. The variance of the error is zero for all inputs.
2. (X) The variance of the error is constant for all inputs.
3. The variance of the error is linear with respect to the input vector size $||x||$.
4. The variance of the error is logarithmic with respect to the input vector size $||x||$.


## Select a false statement about the softmax function

1. $\operatorname{softmax}(\boldsymbol{x}) = \frac{\exp \boldsymbol{x}}{\sum_i \exp x_i}$
2. Softmax is invariant towards shift: $\operatorname{softmax}(\boldsymbol{x} + c) = \operatorname{softmax}(\boldsymbol{x})$
3. (X) Softmax is invariant towards shift: $\operatorname{softmax}(\boldsymbol{x} + c) = \operatorname{softmax}(\boldsymbol{x})$ + c
4. Softmax yields a categorical distribution.


## Generalized linear models

1. (X) Are a special case of neural networks with zero hidden layers.
2. Always have the optimum analytical solution on training data.
3. With $D$-dimensional input have the same number of parameters as a multi-layer perceptron with $D$-dimensional input and $D$ hidden units.
4. Can only work with linear features, they do not converge with polynomial features.


## The hidden layer of MLP $\boldsymbol{h}$

1. Can be interpreted as automatic features extraction from $\boldsymbol{x}$. Vector $\boldsymbol{h}$ is a logarithm of a multinomial distribution over the so called hidden features.
2. (X) $\boldsymbol{h} = a(\boldsymbol{x}^T\boldsymbol{W} + b)$ where $a$ is the activation function.
3. $\boldsymbol{h} = \lambda\boldsymbol{x}_A + (1 - \lambda)\boldsymbol{x}_B$ for all $A$, $B$ such that $t_A = t_B$ (i.e., $\boldsymbol{x}_A$ and $\boldsymbol{x}_B$ belong to the same class).
4. Is only used during training. At inference time, it is removed (hidden) and MLP behaves as a linear model.


## Select a false statement about activation functions in multi-layer perceptron.

1. The activation functions must be continuous (almost everywhere), so we can use SGD for training.
2. The most frequently used activation functions for hidden layers are $\tanh$ and $\operatorname{ReLU}$.
3. One of the problems with sigmoid as activation function is that $\sigma'(0) = \frac{1}{4}$.
4. (X) Identity is the best activation function because it is has a constant derivation. This helps avoiding gradients smaller than 1.


