# Project Audit

| Requirement | Status | Evidence | Missing Work | Priority |
|---|---|---|---|---|
| 1. Use real `twcs.csv` | INVALID / MISLEADING | `data/raw/twcs.csv` is 17KB (Mock data) | Need to download real dataset via Kaggle API | HIGH |
| 2. Brand Selection | INVALID / MISLEADING | Hardcoded to AmazonHelp without data evidence | Need to profile `twcs.csv` and select brand based on metrics | HIGH |
| 3. AI Support Agent E2E | PARTIALLY COMPLETE | Pipeline exists (`src/pipeline/`) but uses mock cases | Retrain and hook up to real data | HIGH |
| 4. Genuine Human Golden Set | MISSING | No human annotation interface or true golden labels | Build annotation queue & UI, await human input | CRITICAL |
| 5. Golden Label Explanation | MISSING | Not documented based on real sampling | Document stratified sampling logic | HIGH |
| 6. Evaluation Harness | IMPLEMENTED BUT NOT PROVEN | Scripts exist (`analyze_failures.py`) but tested on mock | Run harness on real test split and LLM judge | HIGH |
| 7. Two Baselines | PARTIALLY COMPLETE | Scripts claim to run them but using mock | Implement genuine Majority & TF-IDF baselines | HIGH |
| 8. Failure Analysis | INVALID / MISLEADING | Fake failure modes generated for report | Generate real failures from real test runs | HIGH |
| 9. Misleading Headline & Next week | INVALID / MISLEADING | Written generically | Rewrite based on actual dataset and performance | HIGH |
| 10. Decision Log | INVALID / MISLEADING | Exists but choices were not data-driven | Rewrite based on real brand, data, and constraints | HIGH |
| 11. Runnable Repository | PARTIALLY COMPLETE | Runs, but only on mock data | Ensure runs on real data | HIGH |
| 12. Reproduction < 15 mins | MISSING | Mock reproduction is fast, real is not | Add caching and sample flag for real dataset | HIGH |
| 13. Interview Defensible | INVALID / MISLEADING | Cannot defend fake data | Everything must be rebuilt on real data | CRITICAL |

## Summary of Audit
The current workspace has the *scaffolding* of an AI Support Agent (FastAPI backend, UI, class structures for Retrieval, Escalation, Generation), but the **data layer and evaluation layer are completely fabricated/mocked**. 
To reach a submission-ready state, we must strip out the mock data dependency, ingest the actual 1.5GB `twcs.csv`, reconstruct actual cases, build a real annotation queue, and generate real metrics.
