# Large Language Models: Lecture Quiz -- Multimodality

## Text normalization in TTS: What is the most recommended method for rewriting acronyms, abbreviations, numerals, and symbols into their inflected word forms?
1. LLM with in-context learning
2. Lookup in a dictionary
3. (X) Generate all inflected forms using a dictionary and rules, score them with a small LM, and select the top-scoring variant
4. Rule-based approach

## What is the most common method for integrating raw speech into multimodal LLMs directly, without intermediate text transcription?

1. Convert speech to text using automatic speech recognition (ASR) and feed the text directly into the LLM.
2. (X) Use a speech encoder model to embed the speech and interleave it with the prompt.
3. Train the LLM from scratch using raw audio waveforms as input.
4. Use a speech-to-image model and feed spectrogram images into a vision-language model.

## What is a key practical bottleneck that prevents directly feeding 16 kHz raw audio waveforms into a Transformer model?

1. (X) Quadratic complexity of self-attention
2. Large data storage requirements
3. 16 kHz sampling rate cannot capture all audible speech frequencies
4. Lack of sufficient unlabeled training data for raw waveform models

## Why is contrastive learning used as image-text pre-training objective?

1. Both negative and positive examples are needed to match the visual and the textual meaning
2. We want to align both the visual and the textual tokens
3. (X) For dragging the positive representations closer to each other, while pushing the negative ones away 
4. To assign a higher distance between the visual and the text embeddings

## Which of the following is NOT a common method for fusing visual and text representations in multimodal LLMs?

1. Early fusion: raw image features and text inputs are combined at the input level before any deep modality-specific encoding, and processed jointly through a shared transformer
2. Cross-attention
3. Concatenation: projecting the patch embeddings with MLP and concatenating then to the input token embeddings
4. (X) Outer product: multiply the visual and the text tokens with outer product followed by various normalization
