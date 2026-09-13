import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_dataset():
    data_path = os.path.join("data", "raw", "twcs.csv")
    
    # Check if a sufficiently large dataset already exists
    if os.path.exists(data_path):
        size_mb = os.path.getsize(data_path) / (1024 * 1024)
        if size_mb > 100:
            logger.info(f"Real dataset already exists at {data_path} ({size_mb:.2f} MB). Skipping download.")
            sys.exit(0)
        else:
            logger.warning(f"Found {data_path} but it is only {size_mb:.2f} MB. This is a mock dataset.")
            logger.info("Proceeding to download the real dataset from Hugging Face...")
            os.remove(data_path)
    
    try:
        from datasets import load_dataset
        import pandas as pd
    except ImportError:
        logger.error("Required libraries 'datasets' and 'pandas' are not installed. Run `pip install datasets pandas`.")
        sys.exit(1)
        
    logger.info("Downloading the full 'Customer Support on Twitter' dataset from Hugging Face...")
    logger.info("This dataset contains ~2.8M tweets. We will save a robust subsample to disk.")
    
    # Download from the verified mirror that contains full conversational metadata
    dataset = load_dataset('SunidhiSriram/twcs', split='train')
    
    # Convert to pandas
    logger.info("Converting dataset to pandas DataFrame...")
    df = dataset.to_pandas()
    
    # We will use a 500k subsample to ensure fast reproduction times while retaining robust data
    # (as permitted by the assignment rules: "a subsample is expected and encouraged")
    subsample_size = min(500000, len(df))
    logger.info(f"Extracting {subsample_size} rows for the project workspace...")
    df_sub = df.head(subsample_size)
    
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    df_sub.to_csv(data_path, index=False)
    
    final_size_mb = os.path.getsize(data_path) / (1024 * 1024)
    logger.info(f"SUCCESS: Real dataset subsample saved to {data_path} ({final_size_mb:.2f} MB).")

if __name__ == "__main__":
    download_dataset()
