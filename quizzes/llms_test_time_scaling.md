# Large Language Models: Lecture 10 Quiz -- Test-Time Scaling

## According to the "Chinchilla scaling laws" (Hoffmann et al., 2022), how should resources be allocated for compute-optimal training?

1. The model size should increase exponentially while the number of training tokens should scale linearly.
2. The number of training tokens should scale linearly while model size remains constant.
3. The model size should increase linearly while the number of training tokens should linearly decrease.
4. (X) The model size and the number of training tokens should be scaled equally.


## What is test-time scaling?

1. Increasing a model's parameter count and training data during pretraining for more efficient inference.
2. Overtraining a smaller model on a larger dataset to reduce its computational cost at inference time.
3. (X) Improving a model's performance by using more compute at inference time, such as generating multiple reasoning paths and selecting the best one.
4. Validating reasoning traces with an external verifier for creating synthetic reasoning data.


## What is the main idea behind chain-of-thought prompting?

1. It verifies the final answer of the model.
2. (X) It encourages the model to generate intermediate reasoning steps for solving complex problems.
3. It trains a reasoning model that generates intermediate reasoning steps before every answer.
4. It forces the model to retrieve external documents before answering.


## In a RAG pipeline, what happens after relevant document chunks are retrieved for the user prompt?

1. The chunks are concatenated with the model's answer.
2. The chunks are verified by a reasoning model.
3. The chunks are stored in a vector database.
4. (X) The chunks are added to the user prompt.


## What is the Model Context Protocol (MCP)?

1. (X) A standardized JSON-based protocol for describing and accessing external tools.
2. A protocol that trains LLMs to call tools using synthetic training examples.
3. A specification for structured outputs that enforces valid JSON in model responses.
4. A method that reduces the number of tokens used by tool descriptions in the context window.
