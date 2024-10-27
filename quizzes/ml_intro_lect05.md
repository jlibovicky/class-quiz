# Intro to ML: Lecture 5 Recap (Universal Approximation Theorem, Derivation of Sofmax, F-Score)

## In a classification model with softmax output and using negative log-likelihood (NLL) loss, what is the derivative of the NLL loss with respect to the input to the softmax function for class $j$ when the true class is $k$?

1. $\text{softmax}(j) \cdot (1 - \text{softmax}(k))$
2. (X) $\text{softmax}(j)$ if $j \neq k$, and $\text{softmax}(j) - 1$ if $j = k$
3. $-\frac{1}{\text{softmax}(j)}$ for all $j$
4. $\frac{\partial \text{softmax}(k)}{\partial x_j} \cdot \text{softmax}(j)$


## Which of the following is true about the Universal Approximation Theorem when using ReLU activation functions?

1. Multilayer perceptron can approximate any continuous function on a closed interval regardless of the hidden layer size.
2. (X) A multi-layer neural network with a sufficient number of hidden units can approximate any continuous function on a closed interval.
3. Only networks with $\tahn$ activations can approximate continuous functions.
4. The theorem only applies to networks trained on large datasets.


## To find the minimum of a function $f(x)$ subject to a constraint $g(x)=0$, which method is typically used?

1. We take the derivative of $f(x)$ with respect to $x$, set it to zero, and solve for $x$ and select a solution that satisfies the constraint.
2. We set the gradient of $f(x)$ to be orthogonal to the gradient of $g(x)$ and solve for $x$.
3. We do a numeric approximation using SGD.
4. (X) We take derivative of $f(x) - \lambda g(x)$ by $x$ and $\lambda$, set them to zero and solve the corresponding equations.


## Why is the softmax function used in classification models often referred to as a "maximum entropy classifier"?

1. Because it assigns higher probabilities to classes with lower entropy, balancing the probability mass.
2. Because it ensures the highest entropy by producing a uniform distribution across all possible classes.
3. (X) Because it produces a categorical distribution with maximum entropy while preserving the average feature values for each class in the training data.
4. Because it minimizes the cross-entropy of the predictions on the training set.


## In terms of true positives (TP), false positives (FP), false negatives (FN), and true negatives (TN), how are precision and recall defined?

1. Precision = $\frac{\text{TP}}{\text{TP} + \text{FN}}$; Recall = $\frac{\text{TP}}{\text{TP} + \text{FP}} \)
2. (X) Precision = $\frac{\text{TP}}{\text{TP} + \text{FP}}$; Recall = $\frac{\text{TP}}{\text{TP} + \text{FN}} \)
3. Precision = $\frac{\text{TP}}{\text{TP} + \text{TN}}$; Recall = $\frac{\text{TP}}{\text{TP} + \text{FP}} \)
4. Precision = $\frac{\text{TP} + \text{FP}}{\text{TP}}$; Recall = $\frac{\text{TP} + \text{FN}}{\text{TP}} \)


## When precision is 1% and recall is 100%, what is the value of F-score?

1. (X) 1.98%
2. 10%
3. 50.5%
4. 100%
