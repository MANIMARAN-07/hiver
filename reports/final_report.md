# Final Report: AI Customer Support Agent

## Overview
This project implements an evidence-driven, confidence-aware AI customer support agent trained on the Customer Support on Twitter dataset.

## What is Misleading About My Headline Number?
If we claim an "80% Macro-F1 Score" or a "90% Accuracy", it would be misleading for several reasons:
1. **Selective Evaluation Set**: The quality filter drops many messy, unstructured cases. High accuracy on clean cases does not translate to production.
2. **Historical Data Limitations**: The cases retrieved are historical. Policy changes over time. A reply might be historically accurate but currently wrong, which standard metrics wouldn't catch.
3. **Class Imbalance**: An intent like "Hardware Support" might dominate the dataset, allowing a classifier to achieve high accuracy simply by guessing the majority class.
4. **Coverage vs Risk**: A 100% automation rate would lead to massive hallucinations. The real metric is the **Safe Auto-Handle Rate** (which was observed to be ~20% in the sample run).

## Headline Metric Selection
**Headline Metric**: Safe Auto-Handle Rate (at zero tolerance for ungrounded claims).

*Why?* In a support setting, doing nothing (escalating) is vastly preferable to doing something wrong (inventing a refund). Therefore, maximizing the auto-handle rate *subject to* a strict confidence and grounding constraint is the most business-relevant metric.

## One-Week Plan
What I would do with one more week:
1. **Improve Contradiction Detection**: Add an NLI model to check if historical cases contradict each other before passing them to the LLM.
2. **Better Calibration**: Implement Isotonic Regression on a dedicated validation set to make intent probabilities reflect true likelihoods more accurately.
3. **Hybrid Retrieval**: Add BM25 retrieval to augment the FAISS vector search, specifically for queries involving exact error codes or serial numbers where semantic search struggles.
4. **Human Feedback Loop**: Integrate the LLM judge's disagreements with the human annotations into a weak-supervision loop to refine the prompt.

## Performance
- **Embedding Latency**: ~15ms per message.
- **Retrieval Latency**: <5ms (FAISS Flat L2 on small index).
- **LLM Latency**: Provider dependent (~1-2 seconds for GPT-4o-mini).
- **Total E2E Latency**: ~2.5 seconds per message.
