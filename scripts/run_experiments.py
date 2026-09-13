import os
import yaml
import json
import argparse
from pathlib import Path
from src.data.loader import load_dataset
from src.data.cases import reconstruct_conversations, filter_quality_cases
from src.pipeline import SupportAgentPipeline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true", help="Run a quick sample")
    args = parser.parse_args()

    with open("configs/default.yaml", "r") as f:
        config = yaml.safe_load(f)
        
    raw_path = config["dataset"]["raw_data_path"]
    brand = config["brand"]["selected_brand"]
    artifacts_dir = Path(config["paths"]["artifacts"])
    
    df = load_dataset(raw_path)
    cases = reconstruct_conversations(df, brand)
    quality_cases = filter_quality_cases(cases)
    
    if args.sample:
        quality_cases = quality_cases[:10]
        
    if not quality_cases:
        print("No cases to evaluate.")
        return
        
    pipeline = SupportAgentPipeline(
        model_dir=str(artifacts_dir / "models"),
        retrieval_dir=str(artifacts_dir / "retrieval"),
        config=config
    )
    
    results = []
    escalated = 0
    auto_handled = 0
    grounded_count = 0
    
    print(f"Running evaluation on {len(quality_cases)} cases...")
    for case in quality_cases:
        res = pipeline.run(case["customer_message"])
        results.append(res)
        
        if res["decision"] == "ESCALATE":
            escalated += 1
        else:
            auto_handled += 1
            
        if res["is_grounded"]:
            grounded_count += 1
            
    # Metrics
    total = len(quality_cases)
    metrics = {
        "total_cases_evaluated": total,
        "auto_handle_rate": auto_handled / total if total > 0 else 0,
        "escalation_rate": escalated / total if total > 0 else 0,
        "grounded_rate": grounded_count / total if total > 0 else 0
    }
    
    eval_dir = artifacts_dir / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)
    
    with open(eval_dir / "e2e_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
        
    print(json.dumps(metrics, indent=4))
    print("End-to-End Evaluation complete.")

if __name__ == "__main__":
    main()
