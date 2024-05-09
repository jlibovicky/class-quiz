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
