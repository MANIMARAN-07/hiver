import pandas as pd
import numpy as np
import logging
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sentence_transformers import SentenceTransformer
import warnings
from src.intent.auto_label_golden import label_case # We use our heuristic to weak-label train data

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_and_evaluate():
    logger.info("Loading Golden Set for Evaluation...")
    golden = pd.read_csv("data/golden_set/golden_labels.csv")
    y_test = golden['true_intent'].tolist()
    X_test_text = golden['customer_message'].tolist()
    
    logger.info("Loading Training Set and generating weak labels...")
    train = pd.read_csv("data/processed/train.csv").sample(n=5000, random_state=42)
    
    train['weak_intent'] = train['customer_message'].apply(lambda x: label_case(x)[0])
    y_train = train['weak_intent'].tolist()
    X_train_text = train['customer_message'].tolist()
    
    metrics = {}
    
    # ---------------------------------------------------------
    # Baseline 1: Trivial (Majority Class)
    # ---------------------------------------------------------
    logger.info("Evaluating Baseline 1: Majority Class...")
    majority_class = pd.Series(y_train).mode()[0]
    y_pred_b1 = [majority_class] * len(y_test)
    acc_b1 = accuracy_score(y_test, y_pred_b1)
    metrics['baseline_trivial'] = {"accuracy": acc_b1, "majority_class": majority_class}
    
    # ---------------------------------------------------------
    # Baseline 2: Simple (TF-IDF + Logistic Regression)
    # ---------------------------------------------------------
    logger.info("Training Baseline 2: TF-IDF + Logistic Regression...")
    vectorizer = TfidfVectorizer(max_features=2000, stop_words='english')
    X_train_tfidf = vectorizer.fit_transform(X_train_text)
    X_test_tfidf = vectorizer.transform(X_test_text)
    
    lr_tfidf = LogisticRegression(max_iter=1000)
    lr_tfidf.fit(X_train_tfidf, y_train)
    
    y_pred_b2 = lr_tfidf.predict(X_test_tfidf)
    acc_b2 = accuracy_score(y_test, y_pred_b2)
    metrics['baseline_simple'] = {"accuracy": acc_b2}
    
    # ---------------------------------------------------------
    # Main Model: SentenceTransformers + Logistic Regression
    # ---------------------------------------------------------
    logger.info("Training Main Model: SentenceTransformers + Logistic Regression...")
    logger.info("Loading all-MiniLM-L6-v2...")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    X_train_emb = embedder.encode(X_train_text, show_progress_bar=False)
    X_test_emb = embedder.encode(X_test_text, show_progress_bar=False)
    
    lr_main = LogisticRegression(max_iter=1000, C=1.0)
    lr_main.fit(X_train_emb, y_train)
    
    y_pred_main = lr_main.predict(X_test_emb)
    acc_main = accuracy_score(y_test, y_pred_main)
    
    report = classification_report(y_test, y_pred_main, output_dict=True)
    metrics['main_model'] = {
        "accuracy": acc_main,
        "classification_report": report
    }
    
    # Save Metrics
    os.makedirs("artifacts/metrics", exist_ok=True)
    with open("artifacts/metrics/classification_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
        
    logger.info(f"Results -> Trivial: {acc_b1:.3f} | TF-IDF: {acc_b2:.3f} | Main: {acc_main:.3f}")
    logger.info("Metrics saved to artifacts/metrics/classification_metrics.json")
    
if __name__ == "__main__":
    train_and_evaluate()
