# Large Language Models: Lecture 2 Recap

## What is the purpose of residual connections in the Transformer architecture?

1. (X) To prevent the gradient from vanishing during training.
2. To replace the need for traditional RNNs and LSTMs.
3. Transformers do use residual connections and use layer normalization instead.

## What does the self-attention mechanism in Transformers allow each token to do?

1. Ignore other tokens for faster processing.
2. Only focus on tokens that are syntactically related.
3. Reduce the computation needed for attention by focusing on a fixed number of tokens.
4. (X) Dynamically consider other tokens in the sequence to better understand context.

## What is the primary function of the feed-forward layer in each Transformer block?

1. To decide which token to focus on in the next generation step.
2. (X) To apply a position-wise dense layer to the output of the attention mechanism.
3. To calculate the attention scores between tokens.
4. To encode the position of each token in the sequence.

## Which of the following best describes the intuition behind the self-attention mechanism in Transformers?

1. (X) To allow tokens to communicate what information they carry to other tokens.
2. To mimic the human ability to focus on one task at a time.
3. To reduce the complexity and computational resources required.
4. To enable the model to run on parallel hardware efficiently.

## How do token embeddings and position embeddings work together in a Transformer model?

1. Token embeddings are added to the model's output, and position embeddings are ignored.
2. Position embeddings replace token embeddings after the self-attention layer.
3. (X) Token embeddings provide the meaning of each token, and position embeddings provide information about the order of tokens.
4. Token embeddings are used during training, while position embeddings are used during inference.

## In the context of Transformer models, what is the significance of multi-head attention?

1. It allows the model to focus on different parts of the sentence at the same time.
2. It increases the model size without improving performance.
3. (X) It enables the model to capture information from different representation subspaces at different positions.
4. It reduces the overall computational complexity of the attention mechanism.

## What is the correct equation for the $i$-th head in the multi-head self-attention for a sequence of hidden states $X = (x_1, \lodts, x_n)$?

1. (X) $\text{softmax}\left(\frac{XW_{Qi} (XW_{Ki})^T}{\sqrt{d_k}}\right)XW_{Vi}$
2. $W_2 \cdot a(W_1 \cdot X + b_1) + b_2$
3. $\text{norm}(XX^T)$
4. $\frac{1}{\sigma \sqrt{2\pi} } e^{-\frac{1}{2}\left(\frac{X-\mu}{\sigma}\right)^2}$
