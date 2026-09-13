import pandas as pd
from typing import List, Dict

def reconstruct_conversations(df: pd.DataFrame, target_brand: str) -> List[Dict]:
    """
    Reconstructs conversation threads from raw tweets, targeting a specific brand.
    A support case is: Customer Message -> Support Action -> Customer Resolution (if any).
    """
    print(f"Reconstructing conversations for {target_brand}...")
    
    # Filter tweets that involve the target brand
    brand_tweets = df[df['author_id'] == target_brand].copy()
    brand_tweets['in_response_to_tweet_id'] = brand_tweets['in_response_to_tweet_id'].astype(str).str.replace(r'\.0$', '', regex=True)
    df['tweet_id'] = df['tweet_id'].astype(str).str.replace(r'\.0$', '', regex=True)
    
    inbound_reply_ids = brand_tweets[brand_tweets['in_response_to_tweet_id'] != ""]['in_response_to_tweet_id'].unique()
    inbound_tweets = df[df['tweet_id'].isin(inbound_reply_ids)]
    
    cases = []
    
    # Map for O(1) lookups
    tweet_dict = df.set_index('tweet_id').to_dict(orient='index')
    
    for _, inbound in inbound_tweets.iterrows():
        inbound_id = inbound['tweet_id']
        # Find all responses to this inbound tweet
        responses = brand_tweets[brand_tweets['in_response_to_tweet_id'] == inbound_id]
        
        if responses.empty:
            continue
            
        # Simplest case: 1 inbound -> 1 brand response
        # In a real scenario, we'd recursively trace the thread
        
        brand_response = responses.iloc[0]
        
        case = {
            "case_id": f"case_{inbound_id}",
            "customer_id": inbound['author_id'],
            "customer_message": inbound['text'],
            "support_message": brand_response['text'],
            "created_at": str(inbound['created_at']),
            "brand": target_brand
        }
        cases.append(case)
        
    return cases

def filter_quality_cases(cases: List[Dict]) -> List[Dict]:
    """
    Filters cases based on deterministic quality criteria.
    """
    filtered = []
    for c in cases:
        # Exclude empty
        if not c['customer_message'] or not c['support_message']:
            continue
            
        # Exclude very short messages (e.g., just "@AppleSupport")
        if len(c['customer_message'].split()) < 3:
            continue
            
        filtered.append(c)
        
    return filtered
