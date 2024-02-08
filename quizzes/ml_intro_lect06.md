# Intro to ML: Lecture 6 Recap (TF-IDF, Word2Vec)

## The formula for TF-IDF is

1. $\operatorname{TF-IDF}(t, d) = P(t|d) \log \frac{1}{P(d | t)}$
2. $\operatorname{TF-IDF}(t, d) = -P(t|d) \log \frac{P(d)}{P(d | t)}$
3. $\operatorname{TF-IDF}(t, d) = P(t|d) \left( H(\mathcal{D}) - H(\mathcal{D}|t) \right)$
4. (*) $\operatorname{TF-IDF}(t, d) = P(t|d) \log \frac{P(d)}{P(d | t)}$


## One of the reasons for logarithming the inverse document frequency ($\frac{|\mathcal{D}|}{|d \in \mathcal{D}: t|}$) is

1. It turns IDF into self-information of conditional distribution $P(d | t \in d)$, i.e., choosing document $d$ given that we know that it contains the term $t$.
2. (*) Word frequencies decrease quickly with word rank in language, it would be extremely high for low-frequency words.
3. It ensures that the $L^2$-norm of the TF-IDF vector is always one.
4. It makes the computation faster: the logarithm of fraction is a difference of logarithms.


## We say that neural networks represent words as vectors because

1. Of the famous metaphor with vectors lying in a bed, i.e., embedded, therefore word embeddings.
2. The activations on hidden layers are vectors.
3. (*) They correspond to columns of a weight matrix when the words would be represented as one-hot vectors assuming a finite vocabulary.
4. The weight matrix is much smaller than if we used one-hot vectors with the same vocabulary size.


## Language models

1. (*) Estimate a probability of a token (word, character, ...) given context.
2. Have no probabilistic interpretability and are only used to get word embeddings.
3. Are any neural networks that process text.
4. Are neural networks that have word embeddings both as an input and as an output.


## The skip-gram model with embedding matrix $\boldsymbol{E}$ and output matrix $\boldsymbol{W}$.

1. Predicts a probability of two words appearing after each other as $\sigma\left((\boldsymbol{e} _ i + \boldsymbol{e}_{i+1})^T \boldsymbol{W}\right)$.
2. (*) Predicts the probability that word $w_j$ appears in a context window of the word $w_i$ as $\sigma(\boldsymbol{e} _ i^T \boldsymbol{W}_{\ast,j})$.
3. Uses logistic regression to predict if two words can appear in a given context window, i.e., there is one output matrix $\boldsymbol{W}$ for each word. As a results of this, the skip-gram model has $|V|^3$ parameters where $|V|$ is the vocabulary size.
4. Avoid using logistic regression because logistic regression only learns the parameter $\boldsymbol{W}$, but our goal is learning the embedding matrix $\boldsymbol{E}$.


## A reasonable way how to use word embeddings for part-of-speech tagging would be:

1. Use word embeddings to retrieve similar words for training data augmentation.
2. Use an average word embedding over a sentence to get the overall context and then add one-features that describe each specific word (mostly its prefixes and suffixes).
3. Use only the embedding of the word being classified, so it is not influenced by the context.
4. (*) Use a sliding window over the sentence and predict the tag for the middle word.


