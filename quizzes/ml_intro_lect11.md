# Intro to ML: Lecture 11 Recap (SVD, PCA, k-Means)

## Select a **false** statement about SVD $\boldsymbol X = \boldsymbol U \boldsymbol \Sigma \boldsymbol V^T$ of dimension $m \times n$ ?

1. $\boldsymbol U$ and $\boldsymbol V$ are orthonormal matrices.
2. $\boldsymbol \Sigma$ is a diagonal matrix.
3. The columns of $\boldsymbol U$ are the eigenvectors of $\boldsymbol X \boldsymbol X^T$.
4. (X) $\boldsymbol U^{-1} = \boldsymbol V^T$.


## The Eckart-Young theorem states that

1. (X) the best rank-$k$ approximation of $\boldsymbol X$ is given by $\boldsymbol U_k \boldsymbol \Sigma_k \boldsymbol V_k^T$ where $\boldsymbol U_k$ is the first $k$ columns of $\boldsymbol U$.
2. Removing the smallest singular values of $\boldsymbol X$ will not change the Frobenius norm of $\boldsymbol X$.
3. Removing the smallest singular values of $\boldsymbol X$ will remove the most variance from $\boldsymbol X$.
4. Keeping any $k$ components from SVD will give the same rank-$k$ approximation of $\boldsymbol X$.


## Select a **false** statement about PCA.

1. We cat get the principal components by taking the eigenvectors of the covariance matrix.
2. We can get the principal components by doing SVD of the mean-centered data matrix.
3. The principal components are orthogonal.
4. (X) The number of principal components is equal to the number of features.


## PCA is a method for

1. dimensionality reduction.
2. data compression.
3. data visualization.
4. (X) all of the above.


## The power iteration algorithm computes the eigenvector with the highest eigenvalue

1. multiplying the matrix by itself until convergence, the eigenvector is then the average of the columns of the resulting matrix.
2. iteratively multiplying the matrix by a random vector.
3. computing SVD of different powers of the matrix.
4. (X) iteratively multiplying a random vector by the matrix and normalizing the result.


## The two stages of $k$-means clustering are

1. assigning points to clusters (to the nearest centers) and updating cluster sizes.
2. (X) assigning points to clusters and updating cluster centers.
3. assigning points to clusters and rescaling the data, so the centers are orthogonal.
4. assigning points to clusters and updating cluster sizes, so each cluster has the same number of points regardless of the distance.


## The $k$-means clustering algorithm

1. always converges to the global optimum.
2. (X) converges to a local optimum.
3. converges to the same optimum regardless of the initialization.
4. hierarchically joins nearest clusters.


