<<<<<<< HEAD
# Large Language Models: Lecture 10 Quiz (Speech)

## Why is a practical bottleneck for not directly inputting 16 kHz wav into Transformer?

1. (X) Quadratic complexity of self-attention
2. Data storage space
3. 16kHz can not record the sensible speech frequencies
4. Not enough unlabeled training data

## What is **NOT** the advantage of MFCC over Wav2vec?

1. (X) Noise sensitivity
2. Interpretability
3. Data dependency
4. Computational cost

## What is **NOT** a spectrogram?

1. Human eye readable representation of speech
2. (X) A soundwave plot: air vibration vs. time
3. Fourier decomposition of sound wave into frequencies
4. A soundwave heatmap: vibration frequency intensity vs. time

## What is **NOT** included in latency of simultaneous translation?

1. Time between the word was produced by the speaker and system translating the corresponding word.
2. The transmission time between system components
3. Waiting for the correct translation context
4. Model processing time
5. (X) Time between the word was translated and presented to the user

## How can we say which simultaneous policy is better? Which of their attributes do we compare?

1. (X) The latency-quality trade-off on a test set
2. Their translation quality
3. Their latency
4. The number of citations

## What is the advantage of LocalAgreement simultaneous policy over wait-k?

1. Maximum wait time is limited
2. (X) Self-adaptive wait time by language and content complexity
3. It is more recent
4. Does not assume equal source and target length
=======
# Large Language Models: Lecture 10 Quiz


## What are the main ideas behind the Toolformer model?
1. Integrating external tools into a language model to improve its arithmetic and factual accuracy capabilities.
2. Reducing the size of a language model while maintaining its performance through efficient pruning techniques.
3. Training a language model exclusively on code repositories to enhance its programming capabilities.
4. Developing a language model that operates without any human supervision by using reinforcement learning.


## What is a good practice when evaluating closed-source LLMs?

1. Always use a different test set.
2. (X) Always consult the service data policy to avoid test data leakage.
3. Evaluate in monthly intervals and check the improvements.
4. Introduce artifical noise in the test set to avoid data leakage.


## In natural language inference, what is "entailment"?

1. When one sentence logically contradicts another sentence.
2. When one sentence is less informative than another sentence.
3. (X) When one sentence logically follows from another sentence.
4. When one sentence is unrelated to another sentence.


## Given limited time, which aspects should you prioritize when deciding whether to read an academic paper?

1. The number of pages in the paper and the journal's impact factor.
2. (X) The paper's abstract, relevance to your research question, and the credibility of the authors.
3. The popularity of the paper on academic social networks and the diversity of its references.
4. The paper's publication date and the number of figures and tables included.
>>>>>>> 09f36d1 (quiz 10)
