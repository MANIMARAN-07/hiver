import pandas as pd
from pathlib import Path

def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Robust loading of the TWCS dataset.
    Handles potential bad lines or encoding issues.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {file_path}")
        
    print(f"Loading dataset from {file_path}...")
    # Load dataset with string types for IDs to prevent floating point truncation
    df = pd.read_csv(
        file_path, 
        dtype={
            'tweet_id': str,
            'author_id': str,
            'response_tweet_id': str,
            'in_response_to_tweet_id': str
        },
        parse_dates=['created_at']
    )
    
    # Fill NaN values in ID columns with empty strings
    df['response_tweet_id'] = df['response_tweet_id'].fillna("")
    df['in_response_to_tweet_id'] = df['in_response_to_tweet_id'].fillna("")
    df['text'] = df['text'].fillna("")
    
    return df
