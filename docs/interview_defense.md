# Interview Defense

## Architecture Explanation
The pipeline is designed as a linear sequence of safety checks:
`Message -> Intent Classifier -> FAISS Retrieval -> Evidence Check -> LLM Generation -> Grounding Check -> Escalation Policy`.
This ensures that at no point does the LLM act autonomously without deterministic boundaries.

## Why Each Technology?
- **Python / Pandas**: Standard for data engineering. Robust enough for this scale.
- **SentenceTransformers (`all-MiniLM-L6-v2`)**: Extremely fast, runs locally on CPU, strong semantic representations.
- **FAISS**: The fastest local vector index. No need for a hosted vector database (like Pinecone) for a few thousand cases.
- **Logistic Regression**: Easy to calibrate using Platt scaling, fast to train, interpretable coefficients.
- **GPT-4o-mini**: Cost-effective for the generation task while adhering strictly to structured JSON schemas.

## Evaluation
- **Why Macro-F1?** Customer support datasets are heavily skewed towards generic issues. Macro-F1 prevents the model from ignoring critical but rare intents.
- **Why LLM Judge?** Evaluating helpfulness and correctness is impossible with ROUGE/BLEU. An LLM judge with a strict rubric correlates better with human judgment.

## Failure Analysis Defense
We isolated failures not by blaming the LLM, but by tracing the component. E.g., if a hallucination occurred, the **Grounding Check** failed to catch it, rather than just "the LLM hallucinated".

## Likely Questions & Answers
**Q:** Why didn't you use LangChain?
**A:** LangChain adds unnecessary abstraction layers. Directly integrating OpenAI + FAISS reduces the chance of hidden bugs and makes the execution trace completely transparent, which is critical for trustworthy AI.

**Q:** Why not just pass the whole conversation history directly to the LLM?
**A:** Context windows are finite, and LLMs suffer from the "lost in the middle" problem. Explicit case-level retrieval ensures only highly relevant evidence is supplied.
