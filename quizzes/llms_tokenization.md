# Large Language Models: Lecture Quiz -- Tokenization

## What is the main reason why using individual words as vocabulary units is problematic for LLMs?

1. Words are too short to carry meaningful semantic information
2. (X) There are too many of them and rare words have undertrained embeddings
3. Word boundaries are ambiguous in most languages
4. Words cannot represent punctuation and special characters

## What is the initial state of the vocabulary at the beginning of BPE training?

1. All words in the training corpus
2. The most frequent subword units
3. All possible byte pairs
4. (X) Individual characters only

## Which of the following best describes the BPE merge strategy?

1. Randomly select pairs and merge them until vocabulary size is reached
2. Merge the least frequent neighboring token pair to reduce vocabulary size
3. Merge all pairs that appear more than a given threshold
4. (X) Greedily merge the most frequent neighboring token pair until the desired vocabulary size is reached

## Which language morphology type tends to produce the highest type-token ratio, leading to the most vocabulary sparsity?

1. Isolating (e.g. English, Chinese)
2. Fusional (e.g. Russian, German)
3. (X) Agglutinative (e.g. Turkish, Finnish, Korean)
4. All morphology types produce equal type-token ratios

## What is the practical consequence of oversegmentation for low-resource languages when using LLMs?

1. The model fails to generate text in that language entirely
2. Training data for that language is automatically excluded
3. (X) Higher computation cost, degraded performance, and fewer examples fitting the context window
4. The model switches to character-level predictions for that language
