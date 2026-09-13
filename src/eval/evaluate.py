import pandas as pd
import json
import logging
import os
from sklearn.metrics import accuracy_score, f1_score
from src.pipeline import SupportAgentPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def evaluate_pipeline():
    logger.info("Initializing full Support Agent Pipeline for Evaluation...")
    pipeline = SupportAgentPipeline()
    
    golden_path = "data/golden_set/golden_labels.csv"
    if not os.path.exists(golden_path):
        logger.error(f"Golden set not found at {golden_path}")
        return
        
    df = pd.read_csv(golden_path)
    logger.info(f"Loaded Golden Set with {len(df)} cases.")
    
    results = []
    failures = []
    
    y_true_intent = []
    y_pred_intent = []
    y_true_escalate = []
    y_pred_escalate = []
    llm_scores = []
    
    for idx, row in df.iterrows():
        customer_message = row['customer_message']
        true_intent = row['true_intent']
        true_escalate = row['human_escalate']
        
        try:
            res = pipeline.process(customer_message)
            pred_intent = res['intent']
            pred_escalate = res['needs_escalation']
            reply = res['draft_reply']
            
            # Simple mock judge score
            judge_score = 1.0 if not pred_escalate and "Mock response" not in reply else 0.5
            
            y_true_intent.append(true_intent)
            y_pred_intent.append(pred_intent)
            y_true_escalate.append(true_escalate)
            y_pred_escalate.append(pred_escalate)
            llm_scores.append(judge_score)
            
            if pred_intent != true_intent or pred_escalate != true_escalate:
                failures.append({
                    "message": customer_message,
                    "true_intent": true_intent,
                    "pred_intent": pred_intent,
                    "true_escalate": true_escalate,
                    "pred_escalate": pred_escalate,
                    "reason": res.get('escalation_reason', 'None')
                })
        except Exception as e:
            logger.error(f"Pipeline error on case {row['case_id']}: {e}")
            
    intent_accuracy = accuracy_score(y_true_intent, y_pred_intent)
    escalation_f1 = f1_score(y_true_escalate, y_pred_escalate)
    avg_llm_score = sum(llm_scores) / len(llm_scores) if llm_scores else 0
    
    logger.info(f"Intent Accuracy: {intent_accuracy:.3f}")
    logger.info(f"Escalation F1: {escalation_f1:.3f}")
    logger.info(f"Average Judge Score: {avg_llm_score:.3f}")
    
    report_data = {
        "intent_accuracy": intent_accuracy,
        "escalation_f1": escalation_f1,
        "avg_llm_score": avg_llm_score,
        "top_failures": failures[:5]
    }
    
    os.makedirs("artifacts/metrics", exist_ok=True)
    with open("artifacts/metrics/final_report_data.json", "w") as f:
        json.dump(report_data, f, indent=4)
        
if __name__ == "__main__":
    evaluate_pipeline()
