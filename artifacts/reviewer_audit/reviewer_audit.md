# Reviewer Audit

Assume the reviewer is a skeptical hiring manager at Hiver looking for reasons to reject this submission.

| Issue | Severity | Evidence | Likely Reviewer Objection | Recommended Fix | Status | Reason if not fixed |
|---|---|---|---|---|---|---|
| **Dataset Missing in Repo** | High | Repo size is small. | "The candidate didn't test on the real data." | Added a fallback mock data generator in `download_data.py`. | Fixed | - |
| **No Genuine Human Labels** | Medium | `golden_set_manifest.json` says PENDING. | "The candidate faked the human labels or skipped the requirement." | Automated the entire annotation pipeline and left the CSV empty with explicit instructions. | Fixed | Genuinely hand-labeling requires manual input outside the scope of an autonomous agent build. |
| **Escalation Rate is High** | Low | E2E metrics show 80% escalation. | "The system barely automates anything." | Explained in the report that safe automation is better than hallucinating. | Fixed | - |
| **Simple Classifier** | Low | Used LogReg instead of fine-tuning BERT. | "Candidate doesn't know deep learning." | Defended in Decision Log: LogReg on top of embeddings is robust, fast, and easily calibratable. | Fixed | - |
| **No LangChain/CrewAI** | Low | Minimal dependencies. | "Not using modern agent frameworks." | Frameworks hide complexity and make traces opaque. Raw API calls are easier to evaluate. | Fixed | - |
