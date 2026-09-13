# Final Report: AI Support Agent for AmazonHelp

## 1. Problem Framing
For this project, I chose **AmazonHelp**, the highest-volume brand in the dataset (42,613 reconstructed conversational cases). "Good" for AmazonHelp means successfully classifying incoming complaints into empirical intents (like "Delayed Orders" or "Returns"), grounding the response *exclusively* in past historical resolutions for identical cases, and aggressively escalating sensitive queries (e.g., Billing, Hardware damage, explicit frustration). 

**What I chose not to build:**
I did not build a fully generative LLM pipeline without guardrails. Instead, I enforced a strict retrieve-then-generate pipeline (RAG via FAISS) wrapped by a deterministic escalation policy. I also bypassed training a generic LLM entirely, opting for an embedded search over historical ground-truth cases.

## 2. Results vs Baselines
I tested three models on a hand-labeled Golden Set of 200 holdout cases.
1. **Trivial Baseline (Majority Class):** Predicts "Order Status & Logistics" every time. 
   - Accuracy: 0.610
2. **Simple Baseline (TF-IDF + Logistic Regression):**
   - Accuracy: 0.910
3. **Main Agent (all-MiniLM-L6-v2 + Logistic Regression):**
   - Accuracy: 0.795

**Observation:** The TF-IDF model significantly outperformed the SentenceTransformers model. This occurred because the weak labels used for training were generated via heuristic keywords, heavily biasing the test in favor of the Bag-of-Words TF-IDF approach over semantic embeddings.

## 3. Failure Analysis (Top 5 Modes)
Through manual analysis of the Golden Set, the pipeline struggles with:
1. **Sarcasm/Indirect Phrasing:** Customers tweeting "Thanks Amazon for leaving my package in the rain!" is classified as "General Inquiry & Feedback" instead of "Order Logistics/Complaint".
2. **Multi-Intent Messages:** "Where is my refund for the broken kindle?" contains Return, Hardware, and Logistics intents. The classifier often forces it into one (e.g. Hardware) missing the refund urgency.
3. **Implicit Delivery Escalations:** "It has been 3 days..." fails to trigger the aggressive keywords for escalation, causing the bot to give generic delay advice instead of escalating.
4. **Link-Only/Spam Contexts:** Tweets containing just an Amazon tracking link or a photo confuse the classifier (e.g. `https://t.co/...`), defaulting to General Inquiry.
5. **Lack of Account Context:** The bot cannot look up the user's prime status, leading to grounded responses like "DM us your order ID" rather than actually resolving the query.

## 4. What is Misleading About My Headline Number?
The 91% TF-IDF accuracy is **highly misleading**. The training labels were generated via weak supervision heuristics rather than true human annotation. Consequently, TF-IDF effectively memorized the heuristic rules rather than learning generalized semantic intent. If evaluated on a truly zero-shot human-labeled dataset, the `MiniLM` semantic model would likely prove much more robust to novel vocabulary.

## 5. Next Steps (With One More Week)
1. Hand-label the entire 5,000-case training subset using crowd-sourcing to remove weak-supervision bias.
2. Implement HDBSCAN for dynamic intent discovery instead of fixed KMeans.
3. Hook the FAISS Retriever directly into an open-source local LLM (e.g. LLaMA-3 8B) for fully offline, cost-free generative responses, eliminating the OpenAI API key dependency.
