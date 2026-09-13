import yaml
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.pipeline import SupportAgentPipeline
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Hiver AI Support Agent API")

# Allow CORS for local UI development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

pipeline = None

@app.on_event("startup")
def load_model():
    global pipeline
    try:
        with open("configs/default.yaml", "r") as f:
            config = yaml.safe_load(f)
        artifacts_dir = Path(config["paths"]["artifacts"])
        
        # Ensure model exists before initializing
        if (artifacts_dir / "models" / "semantic_classifier.pkl").exists():
            pipeline = SupportAgentPipeline(
                model_dir=str(artifacts_dir / "models"),
                retrieval_dir=str(artifacts_dir / "retrieval"),
                config=config
            )
            print("Pipeline loaded successfully.")
        else:
            print("Warning: Model not found. Please train models first.")
    except Exception as e:
        print(f"Error loading pipeline: {e}")

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="AI Pipeline is not loaded. Train the models first.")
    
    try:
        result = pipeline.run(request.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=8000, reload=True)
