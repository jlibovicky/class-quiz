# Large Language Models: Lecture Quiz -- Multimodality

## What are the two primary challenges of using other modalities than text in LLMs?
1. Generative tasks and Real-Time processing.
2. (X) Data Acquisition and Sparse Representations.
3. Cross language and Conversational Agents.
4. Modality Encoding and Modality Adapting.

## What is the traditional neural network speech representation mentioned in the presentation, and what is its typical frame rate?
1. Raw audio; 16k frames/s
2. (X) Mel Frequency Cepstrum Coefficients (MFCC); 100 frames/s
3. Wav2vec 2.0; 10 ms stride
4. Discrete tokens (e.g., Mimi codec); 80ms per token

## Why is feeding 16 kHz raw audio directly into a standard Transformer model challenging, and what solution is typically used?
1. It results in limited features; the solution is using MFCCs.
2. (X) The complexity of self-attention is O(n^2); the solution is downsampling with CNNs.
3. It is not robust to noise; the solution is using a Length Adapter.
4. It causes domain mismatch; the solution is pre-training on synthetic examples.

## What is the most common method for integrating raw speech into multimodal LLMs directly, without intermediate text transcription?
1. Convert speech to text using automatic speech recognition (ASR) and feed the text directly into the LLM.
2. (X) Use a speech encoder model to embed the speech and interleave it with the prompt.
3. Train the LLM from scratch using raw audio waveforms as input.
4. Use a speech-to-image model and feed spectrogram images into a vision-language model.

## What is the primary function of the Mimi Codec in enabling Full-Duplex LLMs?
1. It translates continuous speech representations into MFCCs.
2. It acts as a Length Adapter to shrink audio representations before the LLM.
3. (X) It encodes speech into discrete tokens that are easily understood by LLMs.
4. It uses a Parallel Transformer Architecture to handle temporal alignment.

## How does the Moshi architecture (Mimi + LLM) manage temporal alignment during simultaneous listening and talking?
1. By using a single stream that alternates between listening and talking (Half-duplex).
2. By using a variable duration for each token based on the speaker's speed.
3. (X) By using "PAD" tokens to maintain synchronization, with each token having a fixed duration of 80ms (12.5 tokens/sec).
4. By relying on the Mimi Codec to output only 3 logical parallel streams.
