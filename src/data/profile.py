import pandas as pd
import json
import os
import logging
from src.data.load_data import load_twcs_dataset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def profile_brands(df: pd.DataFrame, top_k: int = 5):
    """
    Profiles the dataset to find the best candidate brands.
    A brand is an outbound author (inbound == False).
    """
    logger.info("Profiling dataset to select the optimal brand...")
    
    # Filter for brand replies
    outbound_tweets = df[df['inbound'] == False]
    
    # Count replies per brand
    brand_counts = outbound_tweets['author_id'].value_counts()
    
    top_brands = brand_counts.head(top_k)
    logger.info(f"Top {top_k} Brands by Reply Volume:\n{top_brands}")
    
    # For the assignment, we select the top brand (which is typically AmazonHelp or AppleSupport)
    # as it will have the highest likelihood of providing rich, reconstructed conversational cases.
    selected_brand = top_brands.index[0]
    total_brand_replies = int(top_brands.iloc[0])
    
    selection_reasoning = (
        f"Selected {selected_brand} because it has the highest volume of outbound support replies "
        f"({total_brand_replies} replies in the subsample). This ensures maximum availability of "
        f"multi-turn conversational cases (Problem -> Resolution) required to build the Golden Set "
        f"and FAISS retrieval index."
    )
    
    logger.info(selection_reasoning)
    
    # Save the decision to artifacts
    os.makedirs("artifacts/brand_selection", exist_ok=True)
    with open("artifacts/brand_selection/brand_selection.json", "w") as f:
        json.dump({
            "selected_brand": selected_brand,
            "reply_volume": total_brand_replies,
            "alternatives_considered": top_brands.to_dict(),
            "reasoning": selection_reasoning
        }, f, indent=4)
        
    return selected_brand

if __name__ == "__main__":
    try:
        # We process a 500k subsample to ensure fast reproduction times while retaining robust data
        df = load_twcs_dataset(subsample_size=500000)
        selected_brand = profile_brands(df)
        print(f"\nFinal Selected Brand: {selected_brand}")
    except Exception as e:
        logger.error(f"Cannot run profiling: {e}")
