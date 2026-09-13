import os
import yaml
import json
import pickle
from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from src.data.loader import load_dataset
from src.data.cases import reconstruct_conversations, filter_quality_cases
from src.intent.classifier import SemanticClassifier, BaselineClassifier

def main():
    with open("configs/default.yaml", "r") as f:
        config = yaml.safe_load(f)
        
    raw_path = config["dataset"]["raw_data_path"]
    brand = config["brand"]["selected_brand"]
    artifacts_dir = Path(config["paths"]["artifacts"])
    
    # Load cases
    df = load_dataset(raw_path)
    cases = reconstruct_conversations(df, brand)
    quality_cases = filter_quality_cases(cases)
    
    if len(quality_cases) < 10:
        print("Not enough data to train. Exiting.")
        return
        
    # We load taxonomy to assign pseudo-labels for training (as this is a mock dataset)
    with open(artifacts_dir / "intents" / "intent_taxonomy.json", "r") as f:
        taxonomy = json.load(f)
        
    # Heuristic labeling based on inclusion criteria to create training data
    def assign_label(text):
        text_lower = text.lower()
        for intent in taxonomy:
            if any(kw in text_lower for kw in intent["inclusion_criteria"]):
                return intent["name"]
        return "General Inquiry"
        
    texts = [c["customer_message"] for c in quality_cases]
    labels = [assign_label(t) for t in texts]
    
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
    
    # 1. Baseline
    print("Training Baseline TF-IDF + LogReg...")
    baseline = BaselineClassifier()
    baseline.fit(X_train, y_train)
    y_pred_base = baseline.predict(X_test)
    
    # 2. Semantic
    print("Training Semantic Classifier...")
    semantic = SemanticClassifier(config["modeling"]["embedding_model"])
    semantic.fit(X_train, y_train)
    y_pred_sem = semantic.predict(X_test)
    
    # Evaluate
    eval_dir = artifacts_dir / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)
    
    metrics = {
        "baseline": {
            "accuracy": float(accuracy_score(y_test, y_pred_base)),
            "report": classification_report(y_test, y_pred_base, output_dict=True, zero_division=0)
        },
        "semantic": {
            "accuracy": float(accuracy_score(y_test, y_pred_sem)),
            "report": classification_report(y_test, y_pred_sem, output_dict=True, zero_division=0)
        }
    }
    
    with open(eval_dir / "classification_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
        
    # Save semantic model
    model_dir = artifacts_dir / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    semantic.save(str(model_dir / "semantic_classifier.pkl"))
    
    print("Training complete. Metrics saved.")

if __name__ == "__main__":
    main()
