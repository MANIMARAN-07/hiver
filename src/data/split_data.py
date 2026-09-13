import pandas as pd
import logging
from sklearn.model_selection import train_test_split
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def split_cases(input_path: str = "data/processed/cases.csv"):
    logger.info("Loading reconstructed cases for splitting...")
    df = pd.read_csv(input_path)
    
    logger.info(f"Total cases: {len(df)}")
    
    # We use a deterministic random seed to prevent data leakage across runs
    train, temp = train_test_split(df, test_size=0.2, random_state=42)
    val, test = train_test_split(temp, test_size=0.5, random_state=42)
    
    logger.info(f"Split sizes -> Train: {len(train)} | Val: {len(val)} | Test: {len(test)}")
    
    # Save the splits
    train.to_csv("data/processed/train.csv", index=False)
    val.to_csv("data/processed/val.csv", index=False)
    test.to_csv("data/processed/test.csv", index=False)
    
    # Extract 200 cases from the test set for the Golden Set Human Annotation queue
    logger.info("Extracting 200 test cases for the Golden Annotation Queue...")
    golden_candidates = test.sample(n=min(200, len(test)), random_state=101)
    
    os.makedirs("data/golden_set", exist_ok=True)
    golden_candidates.to_csv("data/golden_set/annotation_queue.csv", index=False)
    
    logger.info("Data splitting complete. Golden candidates saved to data/golden_set/annotation_queue.csv")

if __name__ == "__main__":
    split_cases()
