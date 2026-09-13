import pandas as pd
from src.intent.classifier import SemanticClassifier
from src.intent.auto_label_golden import label_case
import os

def save_model():
    print("Loading training data for SemanticClassifier...")
    train = pd.read_csv("data/processed/train.csv").sample(n=5000, random_state=42)
    train['weak_intent'] = train['customer_message'].apply(lambda x: label_case(x)[0])
    
    X = train['customer_message'].tolist()
    y = train['weak_intent'].tolist()
    
    classifier = SemanticClassifier()
    print("Training SemanticClassifier...")
    classifier.fit(X, y)
    
    os.makedirs("artifacts/models", exist_ok=True)
    out_path = "artifacts/models/semantic_classifier.pkl"
    classifier.save(out_path)
    print(f"Saved SemanticClassifier to {out_path}")
    
if __name__ == "__main__":
    save_model()
