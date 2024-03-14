# Intro to ML: Lecture 1 Recap

## What is the difference between classification and regression?

1. (X) Classification predicts **discrete labels**, regression predicts **continuous values**.
2. Classification predicts **continuous values**, regression predicts **discrete labels**.
3. They are different views of **the same problem**, one can be transformed into the other.
4. Classification is **supervised** learning, regression is **unsupervised** learning.


## What is the difference between supervised and unsupervised learning?

1. Unsupervised learning is non-parametric.
2. Supervised learning is non-parametric.
3. (X) Supervised learning uses labeled data, unsupervised learning uses unlabeled data.
4. Learning without supervision is impossible.


## Why is linear regression called linear even when we use it to fit polynomial curves?

1. (X) Because it fits a **hyperplane** in the polynomial feature space.
2. It is **no longer linear** when we use polynomial features.
3. It is linear because it has **linear complexity**.
4. It is linear because it uses** linear algebra** to solve the problem.


## What is overfitting?

1. When the model always predicts the same value regardless of the input.
2. When the model is too simple to fit the data.
3. (X) When the model fits the training data too well, but fails on test data.
4. When the model works perfectly both on training and test data.


## An equation that optimizes $||\boldsymbol{X}\boldsymbol{w} - \boldsymbol{t}||^2$ for $\textbf{w}$ is:

1. (X) $\boldsymbol{w} \leftarrow (\boldsymbol{X}^T\boldsymbol{X})^{-1}\boldsymbol{X}^T\boldsymbol{t}$
2. $\boldsymbol{w} \leftarrow (\boldsymbol{X}^T\boldsymbol{X})(\boldsymbol{X}^T)^{-1}\boldsymbol{t}$
3. It usually has no solution because $\textbf{X}$ is almost never regular.
4. It only has a degenerate solution $\textbf{w} = \textbf{0}$ when we do not add bias term $b$.


## Why is the bias term $b$ missing in the previous equation?

1. (X) It is not missing, it is included in $\boldsymbol{w}$.
2. It is missing because it is always zero.
3. It is missing because it is always one.
4. This a different notation, $b = \boldsymbol{w}$ in this case.


## What is the role of the bias term $b$ in $\boldsymbol{x}^T\boldsymbol{w} + b$?

1. It is the **slope** of the line (or the hyperplane) fitted by the model.
2. (X) It is the **intercept** of the line (or the hyperplane) fitted by the model.
3. It is there to ensure that the predicted value is **always positive**.
4. It is there to ensure that the predicted hyperplane **passes through the origin**.


