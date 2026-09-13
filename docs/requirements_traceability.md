# Requirements Traceability Matrix

| Requirement | Description | Implementation Status | Source Code / Artifact |
|---|---|---|---|
| 0. PRIMARY SOURCE OF TRUTH | Adhere to assignment PDF and track requirements | `READY` | `docs/requirements_traceability.md` |
| 1. AUTOMATION-FIRST RULE | Automate all tasks reliably | `IN_PROGRESS` | All `scripts/` and `src/` |
| 2. HUMAN-JUDGMENT EXCEPTION | Build annotation workflow, never fake labels | `PENDING` | `artifacts/golden/`, `src/evaluation/` |
| 3. NO ARTIFICIAL UNIQUENESS | Use simple stack (Python, scikit, FAISS) | `READY` | `pyproject.toml` |
| 4. REPOSITORY RECONNAISSANCE | Inspect existing code/dataset | `READY` | `artifacts/reconnaissance/project_state.json` (mocked) |
| 5. DATASET HANDLING | Build robust loading code for `twcs.csv` | `PENDING` | `src/data/loader.py` |
| 6. DATA PROFILING | Profile dataset before brand selection | `PENDING` | `src/data/profiling.py`, `artifacts/eda/` |
| 7. BRAND SELECTION | Select ONE brand based on data metrics | `PENDING` | `scripts/select_brand.py` |
| 8. CONVERSATION RECONSTRUCTION | Link tweets into conversations | `PENDING` | `src/data/cases.py` |
| 9. SUPPORT CASES | Build Cases (Problem -> Support -> Resolution) | `PENDING` | `src/data/cases.py` |
| 10. CASE QUALITY FILTERING | Deterministic filters for case quality | `PENDING` | `src/data/cases.py` |
| 11. DATA LEAKAGE PREVENTION | Conversation/temporal splitting | `PENDING` | `tests/test_leakage.py` |
| 12. GOLDEN SET CONSTRUCTION | Sample ~200 cases for evaluation | `PENDING` | `scripts/build_golden_candidates.py` |
| 13. HUMAN ANNOTATION SCHEMA | Define schema for human rating | `PENDING` | `artifacts/golden/annotation_guidelines.md` |
| 14. INTENT DISCOVERY | Discover intents from selected brand's data | `PENDING` | `scripts/discover_intents.py` |
| 15. MULTI-INTENT & AMBIGUITY | Detect ambiguity/multi-intent cases | `PENDING` | `src/intent/classifier.py` |
| 16. BASELINE 1 | Majority class classifier | `PENDING` | `scripts/run_experiments.py` |
| 17. BASELINE 2 | TF-IDF + Logistic Regression | `PENDING` | `scripts/run_experiments.py` |
| 18. MAIN INTENT CLASSIFIER | Semantic embedding + Classifier | `PENDING` | `src/intent/classifier.py` |
| 19. CLASSIFIER CALIBRATION | Calibrate probabilities | `PENDING` | `src/intent/classifier.py` |
| 20. CLASSIFICATION METRICS | Report F1, precision, recall, accuracy | `PENDING` | `src/evaluation/` |
| 21. RETRIEVAL SYSTEM | FAISS + Sentence Transformers | `PENDING` | `src/retrieval/faiss_index.py` |
| 22. RETRIEVAL GRANULARITY | Retrieve at CASE level | `PENDING` | `src/retrieval/faiss_index.py` |
| 23. RETRIEVAL EXPERIMENTS | Evaluate K=1, 3, 5, 10 | `PENDING` | `scripts/run_experiments.py` |
| 24. INTENT-AWARE RETRIEVAL | Compare semantic vs intent-aware | `PENDING` | `src/retrieval/faiss_index.py` |
| 25. HYBRID RETRIEVAL | (Optional) lexical + semantic | `PENDING` | Not prioritized unless needed |
| 26. RERANKING | (Optional) CrossEncoder | `PENDING` | Not prioritized unless needed |
| 27. EVIDENCE SUFFICIENCY | Detect if evidence is sufficient | `PENDING` | `src/retrieval/faiss_index.py` |
| 28. CONTRADICTORY EVIDENCE | Detect contradictions | `PENDING` | `src/retrieval/faiss_index.py` |
| 29. HISTORICAL POLICY WARNING | Cases are evidence, not current policy | `PENDING` | `src/generation/llm_client.py` prompt |
| 30. TEMPORAL AWARENESS | Check behavior changes over time | `PENDING` | `scripts/run_eda.py` |
| 31. LLM GENERATION | Configurable LLM API | `PENDING` | `src/generation/llm_client.py` |
| 32. STRUCTURED OUTPUT | JSON output schema | `PENDING` | `src/generation/llm_client.py` |
| 33. GENERATION RULES | Rules against fabrication, etc. | `PENDING` | `src/generation/llm_client.py` |
| 34. GROUNDING CHECK | Post-generation evidence check | `PENDING` | `src/evaluation/grounding.py` |
| 35. ESCALATION SYSTEM | Deterministic policy layer | `PENDING` | `src/escalation/policy.py` |
| 36. ESCALATION PRINCIPLE | Safe automation over max automation | `PENDING` | `src/escalation/policy.py` |
| 37. HIGH-RISK ESCALATION | Escalate on low confidence/insufficient evidence| `PENDING` | `src/escalation/policy.py` |
| 38. COVERAGE VS RISK | Evaluate selective prediction | `PENDING` | `scripts/run_experiments.py` |
| 39. END-TO-END PIPELINE | E2E integration | `PENDING` | `src/pipeline/__init__.py` |
| 40. FULL TRACEABILITY | Store structured traces | `PENDING` | `src/pipeline/trace.py` |
| 41. EVALUATION ARCHITECTURE | Class/Ret/Gen/Esc/E2E metrics | `PENDING` | `src/evaluation/` |
| 42. LLM-AS-A-JUDGE | Judge against fixed rubric | `PENDING` | `src/evaluation/judge.py` |
| 43. JUDGE BLINDING | Limit judge context to reduce bias | `PENDING` | `src/evaluation/judge.py` |
| 44. JUDGE VERSIONING | Store judge metadata | `PENDING` | `src/evaluation/judge.py` |
| 45. HUMAN VS JUDGE AGREEMENT | Compare human/LLM agreement | `PENDING` | `scripts/analyze_agreement.py` |
| 46. HUMAN EVALUATION AUTOMATION | Automate everything but the judgment | `PENDING` | `artifacts/judge/` |
| 47. FAILURE ANALYSIS | Top 5 failures | `PENDING` | `scripts/analyze_failures.py` |
| 48. FAILURE ATTRIBUTION | Root cause analysis | `PENDING` | `scripts/analyze_failures.py` |
| 49. STRESS TESTS | Automated stress suite | `PENDING` | `tests/test_pipeline.py` |
| 50. RETRIEVAL NEGATIVE TESTS | Negative examples for retrieval | `PENDING` | `tests/test_retrieval.py` |
| 51. ABLATION STUDY | Compare pipelines | `PENDING` | `scripts/run_experiments.py` |
| 52. METRIC LINEAGE | Traceable headline metrics | `PENDING` | `artifacts/metrics/metric_lineage.json` |
| 53. REPRODUCIBILITY | Run in <15 min from sample | `PENDING` | `README.md` |
| 54. CACHE SYSTEM | Cache embeddings, index, LLM outputs | `PENDING` | `src/utils/cache.py` |
| 55. LLM COST CONTROL | Avoid unnecessary LLM calls | `PENDING` | Architecture design |
| 56. API ABSTRACTION | Isolate LLM provider | `PENDING` | `src/llm/base.py` |
| 57. CONFIGURATION | Centralize configs | `READY` | `configs/default.yaml` |
| 58. THRESHOLD TUNING | Tune thresholds on val | `PENDING` | `scripts/train.py` |
| 59. MODEL SELECTION | Justify model | `PENDING` | `docs/decision_log.md` |
| 60. DATA CARD / MODEL CARD | Concise documentation | `PENDING` | `docs/data_card.md`, `docs/model_card.md` |
| 61. SECURITY AND PRIVACY | Do not commit secrets | `READY` | `.env.example`, `.gitignore` |
| 62. TESTING | Unit tests | `PENDING` | `tests/` |
| 63. ERROR HANDLING | Escalate on system errors | `PENDING` | `src/pipeline/__init__.py` |
| 64. OBSERVABILITY | Lightweight logging | `PENDING` | `src/utils/logger.py` |
| 65. PROJECT STRUCTURE | Clean folder structure | `IN_PROGRESS`| Whole repository |
| 66. CLI | Clean scripts/ commands | `PENDING` | `scripts/` |
| 67. DEMO | Streamlit app | `PENDING` | `scripts/run_demo.py` |
| 68. DECISION LOG | 10-15 meaningful decisions | `PENDING` | `docs/decision_log.md` |
| 69. MISLEADING HEADLINE | Honest metric analysis | `PENDING` | `reports/final_report.md` |
| 70. HEADLINE METRIC | Select meaningful headline metric | `PENDING` | `reports/final_report.md` |
| 71. ONE-WEEK PLAN | Proposed future improvements | `PENDING` | `reports/final_report.md` |
| 72. REVIEWER AUDIT | Self-audit as a skeptical reviewer | `PENDING` | `artifacts/reviewer_audit/reviewer_audit.md` |
| 73. SUBMISSION MANIFEST | Checklist of deliverables | `PENDING` | `artifacts/submission/submission_manifest.md` |
| 74. REPRODUCIBILITY AUDIT | Verify reproducibility | `PENDING` | `artifacts/reproducibility/reproduction_report.md` |
| 75. VERSIONING | Track hashes | `PENDING` | `artifacts/version_manifest.json` |
| 76. LICENSE COMPLIANCE | Document dataset license | `PENDING` | `docs/data_card.md` |
| 77. AI DISCLOSURE | Disclose AI-assisted dev | `PENDING` | `docs/ai_assistance.md` |
| 78. INTERVIEW DEFENSE | Interview Q&A | `PENDING` | `docs/interview_defense.md` |
| 79. LIVE MODIFICATION | Guide for modifying code | `PENDING` | `README.md` |
| 80. PERFORMANCE | Runtime and latency | `PENDING` | `reports/final_report.md` |
| 81. QUALITY OVER COMPLEXITY| Only add justifiable complexity | `PENDING` | Ongoing |
| 82. NO FABRICATION RULE | Do not fake data | `PENDING` | Ongoing |
