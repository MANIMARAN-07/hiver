import os
import random
import yaml
import pandas as pd
from pathlib import Path
from src.data.loader import load_dataset
from src.data.cases import reconstruct_conversations, filter_quality_cases

def main():
    with open("configs/default.yaml", "r") as f:
        config = yaml.safe_load(f)
        
    raw_path = config["dataset"]["raw_data_path"]
    brand = config["brand"]["selected_brand"]
    target_size = config["evaluation"]["human_eval_size"]
    artifacts_dir = Path(config["paths"]["artifacts"])
    
    df = load_dataset(raw_path)
    cases = reconstruct_conversations(df, brand)
    quality_cases = filter_quality_cases(cases)
    
    if len(quality_cases) == 0:
        print("No quality cases found. Run EDA first.")
        return
        
    # Sample cases for the golden set
    sample_size = min(target_size, len(quality_cases))
    random.seed(42)
    golden_cases = random.sample(quality_cases, sample_size)
    
    out_dir = artifacts_dir / "golden"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the raw candidates
    df_golden = pd.DataFrame(golden_cases)
    df_golden.to_csv(out_dir / "golden_candidates.csv", index=False)
    
    # Create the annotation template (empty columns for human labels)
    df_template = df_golden[["case_id", "customer_message", "support_message"]].copy()
    df_template["human_intent"] = ""
    df_template["human_auto_handle"] = ""
    df_template["human_escalation_reason"] = ""
    df_template["ambiguity_flag"] = ""
    df_template["optional_notes"] = ""
    
    df_template.to_csv(out_dir / "annotation_template.csv", index=False)
    
    # Write manifest
    import hashlib
    import datetime
    
    manifest = {
        "num_examples": sample_size,
        "sampling_strategy": "random_seed_42",
        "annotation_status": "PENDING_HUMAN_ANNOTATION",
        "version_hash": hashlib.md5(df_template.to_json().encode()).hexdigest(),
        "date_created": str(datetime.datetime.now())
    }
    
    import json
    with open(out_dir / "golden_set_manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)
        
    print(f"Generated {sample_size} golden candidates.")
    print(f"Annotation template saved to {out_dir}/annotation_template.csv")

if __name__ == "__main__":
    main()
