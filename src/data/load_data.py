import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_twcs_dataset(data_path: str = "data/raw/twcs.csv", subsample_size: int = None) -> pd.DataFrame:
    """
    Loads the TWCS dataset. Enforces that the real dataset is present.
    If subsample_size is provided, reads only the first N rows to save memory, 
    as encouraged by the assignment ('a subsample is expected and encouraged').
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Real dataset not found at {data_path}. Please download it from Kaggle.")
        
    size_mb = os.path.getsize(data_path) / (1024 * 1024)
    if size_mb < 50:
        raise ValueError(f"Dataset at {data_path} is only {size_mb:.2f} MB. This is a mock dataset! Strict assignment rules forbid fabricated data.")
    
    logger.info(f"Loading real TWCS dataset ({size_mb:.2f} MB)...")
    
    # Load dataset
    if subsample_size:
        logger.info(f"Subsampling first {subsample_size} rows...")
        df = pd.read_csv(data_path, nrows=subsample_size)
    else:
        df = pd.read_csv(data_path)
        
    logger.info(f"Successfully loaded {len(df)} rows.")
    return df

if __name__ == "__main__":
    # Test the loader (will fail if dataset is missing/mock)
    try:
        df = load_twcs_dataset(subsample_size=10000)
        print(df.head())
    except Exception as e:
        logger.error(str(e))
