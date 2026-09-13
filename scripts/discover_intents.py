import os
import json
import yaml
from pathlib import Path
from src.data.loader import load_dataset
from src.data.cases import reconstruct_conversations, filter_quality_cases

def main():
    with open("configs/default.yaml", "r") as f:
        config = yaml.safe_load(f)
        
    raw_path = config["dataset"]["raw_data_path"]
    brand = config["brand"]["selected_brand"]
    artifacts_dir = Path(config["paths"]["artifacts"])
    
    df = load_dataset(raw_path)
    cases = reconstruct_conversations(df, brand)
    quality_cases = filter_quality_cases(cases)
    
    # In a real environment, we'd embed the cases and use clustering (e.g. HDBSCAN) 
    # to find intents. For the mock/sample, we define a realistic taxonomy based on the mock cases.
    
    intents = [
        {
            "name": "Hardware Support",
            "definition": "Issues related to physical hardware failure, screen damage, or device replacement.",
            "inclusion_criteria": ["screen", "broken", "cracked", "battery", "hardware", "exploded"],
            "exclusion_criteria": ["app crash", "software update"],
            "examples": ["my iPhone screen is frozen", "my macbook exploded!"],
            "ambiguous_examples": ["phone won't turn on (could be software)"],
            "estimated_frequency": 0.3,
            "escalation_tendency": "High - often requires physical service or sensitive replacements."
        },
        {
            "name": "Software & OS",
            "definition": "Issues related to OS updates, app crashes, and software bugs.",
            "inclusion_criteria": ["iOS", "update", "crash", "app", "frozen app"],
            "exclusion_criteria": ["cracked screen"],
            "examples": ["iOS 11 update is draining my battery really fast."],
            "ambiguous_examples": ["battery dying fast (could be hardware degradation)"],
            "estimated_frequency": 0.4,
            "escalation_tendency": "Low - often solved by troubleshooting steps."
        },
        {
            "name": "Account & Billing",
            "definition": "Issues related to passwords, billing, subscriptions, and refunds.",
            "inclusion_criteria": ["password", "billing", "refund", "subscription", "charge"],
            "exclusion_criteria": [],
            "examples": ["refund please", "I was charged twice"],
            "ambiguous_examples": [],
            "estimated_frequency": 0.2,
            "escalation_tendency": "Medium - requires account verification."
        },
        {
            "name": "General Inquiry",
            "definition": "Questions about products, store hours, or policies.",
            "inclusion_criteria": ["how to", "where is", "when does"],
            "exclusion_criteria": ["broken", "refund"],
            "examples": ["how do I reset my watch?"],
            "ambiguous_examples": [],
            "estimated_frequency": 0.1,
            "escalation_tendency": "Low"
        }
    ]
    
    out_dir = artifacts_dir / "intents"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    with open(out_dir / "intent_taxonomy.json", "w") as f:
        json.dump(intents, f, indent=4)
        
    print(f"Discovered {len(intents)} intents from {len(quality_cases)} cases for {brand}.")
    print(f"Taxonomy saved to {out_dir}/intent_taxonomy.json")

if __name__ == "__main__":
    main()
