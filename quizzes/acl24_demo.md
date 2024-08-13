# Large Language Models: Quiz demo for the TeachNLP workshop at ACL 2024


## Which of the following is NOT a component of a Transformer-based language model?

1. (X) Recurrent neural network
2. Decoder
3. Masked self-attention
4. Encoder
5. Positional encoding


## Which of the following models does NOT have an encoder?

1. BERT
2. (X) GPT-3
3. Majority of machine translation models


## Which part of the model is responsible for processing the user prompt of ChatGPT?

1. Encoder
2. Cross-attention
3. (X) Decoder
4. Both encoder and decoder


## Is it possible for tokenized text to have less tokens than the number of words in the original text?

1. Yes, it happens all the time
2. (X) Yes, but rarely
3. Never


## What is the purpose of residual connections in the Transformer architecture?

1. (X) To prevent the gradient from vanishing during training.
2. To replace the need for traditional RNNs and LSTMs.
3. Transformers do not use residual connections and use layer normalization instead.

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

1. (X) Allow tokens to communicate what information they carry to other tokens.
2. Mimic the human ability to focus on one task at a time.
3. Reduce the complexity and computational resources required.
4. Enable the model to run on parallel hardware efficiently.

## How do token embeddings and position embeddings work together in a Transformer model?

1. Token embeddings are added to the model's output, and position embeddings are ignored.
2. Position embeddings replace token embeddings after the self-attention layer.
3. (X) Token embeddings provide the meaning of each token, and position embeddings provide information about the order of tokens.
4. Token embeddings are used during training, while position embeddings are used during inference.

## In the context of Transformer models, what is the significance of multi-head attention?

1. It prevents the model from focusing on different parts of the sentence at the same time.
2. It decreases the model size without affecting the performance.
3. (X) It enables the model to capture information from different representation subspaces at different positions.
4. It reduces the overall computational complexity of the attention mechanism.

## What is the correct equation for the $i$-th head in the multi-head self-attention for a sequence of hidden states $X = (x_1, \ldots, x_n)$?

1. (X) $\text{softmax}\left(\frac{XW_{Qi} (XW_{Ki})^T}{\sqrt{d_k}}\right)XW_{Vi}$
2. $W_2 \cdot a(W_1 \cdot X + b_1) + b_2$
3. $\text{norm}(XX^T)$
4. $\frac{1}{\sigma \sqrt{2\pi} } e^{-\frac{1}{2}\left(\frac{X-\mu}{\sigma}\right)^2}$



## What is the objective for training generative LLMs?

1. Predicting the right token on a masked position inside a target sequence.
2. Predicting the right sequence of tokens given a prefix.
3. (X) Predicting the right token that follows a given prefix.


## Which of the following is the formula for the cross-entropy loss?

1. $\max(0, 1 - \hat{y} \cdot y)$
2. $(y - \hat{y}^2)$
3. (X) $- \frac{1}{|\mathcal{D}|} \sum_{(x,y) \in \mathcal{D}} \log p_{\theta}(y|x)$


## Which of the following is NOT an effect of applying the objective used for training generative LLMs?

1. (X) Increasing the cross-entropy of a one-hot distribution of the correct token
   and the distribution predicted by the model.
2. Increasing the probability of the correct item on the target position.
3. Decreasing the probabilities of incorrect tokens on the target position.
4. Decreasing the cross-entropy of a one-hot distribution of the correct token
   and the distribution predicted by the model.


## Why do training optimizers use momentum?

1. To prevent too high learning rates.
2. To avoid overfitting.
3. (X) To speed up the convergence.
4. Because it guarantees convergence into the global optimum.


## What do we mean by instruction tuning?

1. Instead of using training data, we imperatively tell the model how to update the weights using a dynamic programming algorithm.
2. (X) Formatting the task-specific data as instructions in natural language and using those to further train a pretrained model..
3. Adding sentences that resemble instructions into the training data of the pretrained model.
4. Using human feedback in combination with the reinforcement learning objective.


## What do we use RLHF for?

1. (X) To adapt the model responses to match human preference.
2. To train the model to imitate humans.
3. To prevent overfitting.
4. To decrease the model bias.


## What does it mean when a model is described as "autoregressive"?

1. The model predicts the regression coefficients automatically.
2. The model generates text by conditioning on the entire dataset.
3. (X) The model generates each token by conditioning on the previously generated tokens.
4. The model regresses towards the mean of the training data.

## What is beam search used for in the context of language models?

1. To reduce the computational complexity of the model.
2. To increase the randomness of the text generation.
3. To decrease the diversity of the generated text.
4. (X) To find more likely sequences of text by keeping track of a fixed number of hypotheses.

## Which of the following best describes "top-$k$ sampling"?

1. Sampling from the $k$ **most recent tokens** generated by the model.
2. Sampling from the **entire vocabulary**, then filtering out the top $k$ tokens.
3. (X) Sampling from the $k$ **most likely** next tokens at each step of the generation.
4. Sampling from the **least likely** $k$ tokens to increase output variability.

## How does beam search differ from greedy search?

1. (X) Beam search keeps multiple hypotheses at each step, while greedy search always picks the single best next token.
2. Beam search generates text faster than greedy search.
3. Beam search always produces more coherent text than greedy search.
4. Greedy search can backtrack to previous states, but beam search cannot.

## What problem does nucleus sampling solve that is inherent to top-$k$ sampling?

1. It makes the model faster by reducing the number of tokens considered at each step.
2. (X) It dynamically adjusts the number of tokens considered based on their cumulative probability.
3. It exclusively focuses on the most likely token, thus making the text more predictable.
4. It generates text that is less coherent but more diverse.



## What order of magnitude is the size of contemporary corpora for (pre-)training language models?

1. thousands of tokens
2. millions of tokens
3. billions of tokens
4. (X) trillions of tokens
5. quadrillions of tokens

## Where can one commonly find datasets for NLP tasks?
1. Only from proprietary sources
2. Exclusively through direct data collection efforts
3. (X) Various sources such as online repositories, academic institutions, and web scraping
4. Solely from government agencies


## What are some challenges associated with validating the performance of Natural Language Processing (NLP) models?
1. Subjectivity in human evaluation
2. Limited availability of labeled data for testing
3. Difficulty in defining universal evaluation metrics
4. (X) All of the above


## In NLP, what role do pre-training datasets serve in model development?
1. They provide labeled data for specific tasks
2. (X) They enable models to learn general language representations
3. They serve as test datasets for evaluating model performance
4. They are used primarily for fine-tuning existing models


## What is a potential drawback of relying solely on automatic evaluation metrics such as BLEU or ROUGE in assessing the performance of Natural Language Processing models?
1. (X) Automatic metrics may not capture the nuanced aspects of language understanding, leading to discrepancies between metric scores and human judgments.
2. Automatic metrics often require large computational resources, making them impractical for real-time evaluation of NLP models.
3. Automatic metrics tend to favor models with higher computational complexity, biasing the evaluation towards more resource-intensive approaches.
4. Automatic metrics may overlook the impact of data preprocessing techniques on model performance, resulting in inaccurate assessments of NLP systems.



## Evaluation of LLaMa on multiple choice questions showed that it is very sensitive to exact prompt formulation.

1. LLaMa's performance is unaffected by the way prompts are formulated.
2. (X) LLaMa requires careful prompt design to achieve optimal performance.
3. LLaMa performs equally well with any prompt as long as the context is clear.
4. LLaMa's sensitivity to prompts varies depending on the decoding algorithm.

## When building a chat for question answering...

1. Finding the correct document and searching for the answer within the document are equally challenging.
2. It is more difficult to search for the answer within the document than to find the document itself.
3. (X) Getting the correct document is more challenging than finding the answer once you have the document.
4. Both tasks are simple with advanced language models.

## Why is GPT-4 often used to evaluate outputs of natural language generation?

1. GPT-4 is used because it is the most replicable way of evaluation.
2. Other LLMs can follow instructions, using GPT-4 is just convention.
3. (X) GPT-4 is particularly known for its capability to follow fine-grained instructions.
4. GPT-4 is the only model that can handle low-resource languages effectively.

## What is one of the biggest challenges in simultaneous speech translation?

1. (X) Deciding when to wait or translate, to balance the latency and quality.
2. Distinguishing speech and silence.
3. Different speed of speech in different languages.
4. The computation time of the text-to-text translation.


## What is usually the most in-demand computational resource for fine-tuning LLM?
1. (X) Disk space
2. VRAM (GPU Memory)
3. Inference time
4. RAM (CPU Memory)

## How much GPU memory is approximately needed to fine-tune 10B parameter model (with Adam optimizer)?
1. 16 GB
2. 61 GB
3. (X) 160 GB
4. 610 GB

## LoRA is an algorithm for:
1. (X) Parameter efficient fine-tuning
2. Speeding-up inference
3. Quantization
4. Data compression

## Which of the following is **not** used in qLoRA?
1. Double quantization
2. Low rank adaptation
3. Paged optimization
4. (X) 1.58 bit parameters

## What is the Chinchilla-optimal token to parameter ratio in pre-training?
1. 1:1
2. 2:1
3. 10:1
4. (X) 20:1

## Ability to solve a task in one language after fine-tuning or instructing in another language is attributed to:

1. Forced inference
2. (X) Cross-lingual transfer
3. Reinforcement learning from human feedback
4. Quantization

## Resourcefulness of a language is measured by:

1. (X) Availability of data
2. Number of speakers
3. Linguistics similarity to English
4. Number of unique characters in the writing script


## Which languages are the most prone to over-segmentation:

1. Low-resource, written with Latin script
2. High-resource, written with Latin script
3. (X) Low-resource, written with non-Latin script
4. High-resource, written with non-Latin script

## Which is true about using LLMs for machine translation:

1. Is only possible with GPT-4
2. (X) Can beat dedicated machine translation systems
3. Works better in translating from English than to English
4. Works only for high-resource languages

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




## What are the main ideas behind the Toolformer model?

1. (X) Integrating external tools into a language model to improve its arithmetic and factual accuracy capabilities.
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
