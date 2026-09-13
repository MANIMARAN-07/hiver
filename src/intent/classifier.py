import numpy as np
import pickle
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

class BaselineClassifier:
    """TF-IDF + Logistic Regression Baseline"""
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
        self.clf = LogisticRegression(class_weight='balanced', max_iter=1000)
        self.is_trained = False
        
    def fit(self, X, y):
        X_vec = self.vectorizer.fit_transform(X)
        self.clf.fit(X_vec, y)
        self.is_trained = True
        
    def predict_proba(self, X):
        X_vec = self.vectorizer.transform(X)
        return self.clf.predict_proba(X_vec)
        
    def predict(self, X):
        X_vec = self.vectorizer.transform(X)
        return self.clf.predict(X_vec)
        
class SemanticClassifier:
    """Sentence Transformers + Logistic Regression with Calibration"""
    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(embedding_model_name)
        self.clf = LogisticRegression(class_weight='balanced', max_iter=1000)
        self.is_trained = False
        
    def fit(self, X, y):
        print(f"Encoding {len(X)} texts...")
        X_emb = self.embedder.encode(X, show_progress_bar=True)
        self.clf.fit(X_emb, y)
        self.is_trained = True
        
    def predict_proba(self, X):
        X_emb = self.embedder.encode(X)
        return self.clf.predict_proba(X_emb)
        
    def predict(self, X):
        X_emb = self.embedder.encode(X)
        return self.clf.predict(X_emb)
        
    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self.clf, f)
            
    def load(self, path: str):
        with open(path, "rb") as f:
            self.clf = pickle.load(f)
        self.is_trained = True
