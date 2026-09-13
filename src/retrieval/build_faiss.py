import pandas as pd
import numpy as np
import faiss
import json
import logging
import os
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_index():
    logger.info("Loading training data to build FAISS index for grounded generation...")
    df = pd.read_csv("data/processed/train.csv")
    
    # We take a sample of 20000 cases to keep the index small but highly diverse
    sample_size = min(20000, len(df))
    df = df.sample(n=sample_size, random_state=101)
    
    queries = df['customer_message'].tolist()
    responses = df['support_message'].tolist()
    
    logger.info(f"Encoding {len(queries)} customer messages with SentenceTransformers...")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = embedder.encode(queries, show_progress_bar=True)
    
    dim = embeddings.shape[1]
    logger.info(f"Building FAISS IndexFlatL2 with dimension {dim}...")
    
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
    
    os.makedirs("artifacts/faiss", exist_ok=True)
    faiss.write_index(index, "artifacts/faiss/support_index.bin")
    
    metadata = {
        "responses": responses,
        "queries": queries
    }
    with open("artifacts/faiss/metadata.json", "w") as f:
        json.dump(metadata, f)
        
    logger.info("Successfully built and saved FAISS index and metadata!")

if __name__ == "__main__":
    build_index()
