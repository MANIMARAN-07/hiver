import os
import yaml
from pathlib import Path
from src.data.loader import load_dataset
from src.data.profiling import profile_dataset

def main():
    with open("configs/default.yaml", "r") as f:
        config = yaml.safe_load(f)
        
    raw_path = config["dataset"]["raw_data_path"]
    artifacts_dir = config["paths"]["artifacts"]
    
    eda_dir = Path(artifacts_dir) / "eda"
    eda_dir.mkdir(parents=True, exist_ok=True)
    
    df = load_dataset(raw_path)
    profile_dataset(df, str(eda_dir))

if __name__ == "__main__":
    main()
