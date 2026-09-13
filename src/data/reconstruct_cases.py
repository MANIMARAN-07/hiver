import pandas as pd
import json
import logging
import os
from src.data.load_data import load_twcs_dataset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reconstruct_brand_cases(df: pd.DataFrame, brand_name: str, output_path: str = "data/processed/cases.csv"):
    """
    Reconstructs conversational cases for a specific brand.
    A valid case is: Customer Tweet -> Brand Reply.
    """
    logger.info(f"Reconstructing conversation threads for brand: {brand_name}")
    
    # 1. Get all outbound tweets by the brand
    brand_replies = df[(df['author_id'] == brand_name) & (df['inbound'] == False)].copy()
    logger.info(f"Total raw outbound replies by {brand_name}: {len(brand_replies)}")
    
    # 2. Get all inbound tweets (customer messages)
    inbound_tweets = df[df['inbound'] == True].copy()
    
    # Ensure ID columns are strings for joining
    brand_replies['in_response_to_tweet_id'] = brand_replies['in_response_to_tweet_id'].astype(str).str.replace(r'\.0$', '', regex=True)
    inbound_tweets['tweet_id'] = inbound_tweets['tweet_id'].astype(str)
    
    # 3. Join brand replies with the customer tweets they responded to
    cases = pd.merge(
        inbound_tweets, 
        brand_replies, 
        left_on='tweet_id', 
        right_on='in_response_to_tweet_id',
        suffixes=('_customer', '_support')
    )
    
    # 4. Clean and select relevant columns
    cases = cases[[
        'tweet_id_customer', 'author_id_customer', 'text_customer', 'created_at_customer',
        'tweet_id_support', 'text_support', 'created_at_support'
    ]]
    
    # 5. Quality Filtering (Exclude empty text or missing data)
    cases = cases.dropna(subset=['text_customer', 'text_support'])
    
    # Remove simple acknowledgments as they lack resolution evidence (e.g., "Thanks!", "DM us")
    # A robust filter checks length
    cases = cases[cases['text_support'].str.len() > 20]
    
    # Standardize column names for the pipeline
    cases = cases.rename(columns={
        'tweet_id_customer': 'case_id',
        'text_customer': 'customer_message',
        'text_support': 'support_message'
    })
    
    logger.info(f"Successfully reconstructed {len(cases)} valid cases.")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cases.to_csv(output_path, index=False)
    logger.info(f"Cases saved to {output_path}")
    return cases

if __name__ == "__main__":
    try:
        df = load_twcs_dataset(subsample_size=500000)
        
        # Load selection from artifact if available
        brand_name = "AmazonHelp"
        if os.path.exists("artifacts/brand_selection/brand_selection.json"):
            with open("artifacts/brand_selection/brand_selection.json", "r") as f:
                data = json.load(f)
                brand_name = data.get("selected_brand", "AmazonHelp")
                
        cases = reconstruct_brand_cases(df, brand_name)
    except Exception as e:
        logger.error(f"Cannot reconstruct cases: {e}")
