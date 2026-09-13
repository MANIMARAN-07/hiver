import pandas as pd
import json
from pathlib import Path

def profile_dataset(df: pd.DataFrame, output_dir: str):
    """
    Computes dataset statistics and saves them to artifacts/eda/.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    total_rows = len(df)
    inbound_count = df['inbound'].sum()
    outbound_count = total_rows - inbound_count
    
    # Author stats
    authors = df['author_id'].nunique()
    
    # Brands (usually outbound = False)
    brands = df[df['inbound'] == False]['author_id'].value_counts()
    
    stats = {
        "total_rows": total_rows,
        "total_unique_authors": authors,
        "inbound_tweets": int(inbound_count),
        "outbound_tweets": int(outbound_count),
        "top_brands": brands.head(10).to_dict(),
        "missing_text": int(df['text'].isna().sum()),
        "date_range": {
            "min": str(df['created_at'].min()),
            "max": str(df['created_at'].max())
        }
    }
    
    # Save stats
    with open(Path(output_dir) / "dataset_profile.json", "w") as f:
        json.dump(stats, f, indent=4)
        
    # Save CSV
    brands.to_csv(Path(output_dir) / "brand_distribution.csv")
    
    print(f"Dataset profiling complete. Results saved to {output_dir}")
    return stats
