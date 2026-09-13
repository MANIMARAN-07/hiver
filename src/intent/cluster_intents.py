import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cluster_intents():
    logger.info("Loading training cases...")
    df = pd.read_csv("data/processed/train.csv")
    
    # Take a sample for fast clustering
    sample_size = min(5000, len(df))
    df_sample = df.sample(n=sample_size, random_state=42)
    
    texts = df_sample['customer_message'].tolist()
    
    logger.info("Extracting TF-IDF features...")
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(texts)
    
    num_clusters = 8
    logger.info(f"Clustering into {num_clusters} clusters using KMeans...")
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    
    df_sample['cluster'] = labels
    
    # Print top words per cluster and examples
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    
    print("\n" + "="*50)
    print("INTENT CLUSTERS DISCOVERED FROM DATA")
    print("="*50)
    for i in range(num_clusters):
        top_words = [terms[ind] for ind in order_centroids[i, :10]]
        print(f"\nCluster {i}: {', '.join(top_words)}")
        print("Examples:")
        sample_texts = df_sample[df_sample['cluster'] == i]['customer_message'].head(3).tolist()
        for text in sample_texts:
            safe_text = str(text).encode('ascii', 'ignore').decode('ascii')
            print(f" - {safe_text.replace('\n', ' ')}")
            
if __name__ == "__main__":
    cluster_intents()
