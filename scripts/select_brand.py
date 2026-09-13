import os
import json
import pandas as pd
from pathlib import Path
import yaml

def main():
    with open("configs/default.yaml", "r") as f:
        config = yaml.safe_load(f)
        
    artifacts_dir = Path(config["paths"]["artifacts"])
    brand_dist_file = artifacts_dir / "eda" / "brand_distribution.csv"
    
    if not brand_dist_file.exists():
        print("Run run_eda.py first to generate brand distributions.")
        return
        
    df_brands = pd.read_csv(brand_dist_file, names=['brand', 'count'], header=0)
    
    # We select the brand with the highest volume for stability in this mock/sample environment
    # In a full run, we would factor in conversation depth, etc.
    selected_brand = df_brands.iloc[0]['brand']
    
    out_dir = artifacts_dir / "brand_selection"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    decision = {
        "selected_brand": selected_brand,
        "reason": "Highest volume of outbound support interactions observed in EDA.",
        "data_points": int(df_brands.iloc[0]['count'])
    }
    
    with open(out_dir / "selected_brand.json", "w") as f:
        json.dump(decision, f, indent=4)
        
    print(f"Selected brand: {selected_brand}")
    print(f"Decision logged to {out_dir}/selected_brand.json")
    
    # Update config automatically (simple approach for the exercise)
    with open("configs/default.yaml", "r") as f:
        config_text = f.read()
    
    config_text = config_text.replace('selected_brand: "AppleSupport"', f'selected_brand: "{selected_brand}"')
    
    with open("configs/default.yaml", "w") as f:
        f.write(config_text)

if __name__ == "__main__":
    main()
