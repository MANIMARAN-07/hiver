import faiss
import numpy as np
import pickle
from typing import List, Dict
from sentence_transformers import SentenceTransformer

class CaseRetriever:
    """FAISS-based historical case retrieval."""
    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(embedding_model_name)
        self.index = None
        self.cases = []
        
    def build_index(self, cases: List[Dict]):
        if not cases:
            raise ValueError("No cases provided to build index.")
            
        print(f"Building FAISS index for {len(cases)} cases...")
        self.cases = cases
        texts = [c['customer_message'] for c in cases]
        
        embeddings = self.embedder.encode(texts, show_progress_bar=True)
        dimension = embeddings.shape[1]
        
        # L2 distance index
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        
    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        if self.index is None:
            raise ValueError("Index not built. Call build_index() or load() first.")
            
        query_emb = self.embedder.encode([query]).astype('float32')
        distances, indices = self.index.search(query_emb, k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1 and idx < len(self.cases):
                case = self.cases[idx].copy()
                case['distance'] = float(dist)
                case['similarity_score'] = 1.0 / (1.0 + float(dist)) # Pseudo similarity
                results.append(case)
        return results

    def save(self, path_prefix: str):
        faiss.write_index(self.index, f"{path_prefix}.faiss")
        with open(f"{path_prefix}_cases.pkl", "wb") as f:
            pickle.dump(self.cases, f)
            
    def load(self, path_prefix: str):
        self.index = faiss.read_index(f"{path_prefix}.faiss")
        with open(f"{path_prefix}_cases.pkl", "rb") as f:
            self.cases = pickle.load(f)
