import os
import yaml
from pathlib import Path
from src.data.loader import load_dataset
from src.data.cases import reconstruct_conversations, filter_quality_cases
from src.retrieval.faiss_index import CaseRetriever

def main():
    with open("configs/default.yaml", "r") as f:
        config = yaml.safe_load(f)
        
    raw_path = config["dataset"]["raw_data_path"]
    brand = config["brand"]["selected_brand"]
    artifacts_dir = Path(config["paths"]["artifacts"])
    
    df = load_dataset(raw_path)
    cases = reconstruct_conversations(df, brand)
    quality_cases = filter_quality_cases(cases)
    
    if len(quality_cases) == 0:
        print("No cases to index.")
        return
        
    retriever = CaseRetriever(config["modeling"]["embedding_model"])
    retriever.build_index(quality_cases)
    
    retrieval_dir = artifacts_dir / "retrieval"
    retrieval_dir.mkdir(parents=True, exist_ok=True)
    
    retriever.save(str(retrieval_dir / "case_index"))
    print(f"FAISS index built and saved for {len(quality_cases)} cases.")

if __name__ == "__main__":
    main()
