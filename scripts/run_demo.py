import streamlit as st
import yaml
from pathlib import Path
from src.pipeline import SupportAgentPipeline
import os

st.title("Hiver AI Support Agent Demo")
st.write("Autonomous End-to-End Build")

@st.cache_resource
def load_pipeline():
    with open("configs/default.yaml", "r") as f:
        config = yaml.safe_load(f)
    artifacts_dir = Path(config["paths"]["artifacts"])
    
    # Check if models exist
    if not (artifacts_dir / "models" / "semantic_classifier.pkl").exists():
        st.error("Model not found. Run pipeline first.")
        return None
        
    pipeline = SupportAgentPipeline(
        model_dir=str(artifacts_dir / "models"),
        retrieval_dir=str(artifacts_dir / "retrieval"),
        config=config
    )
    return pipeline

pipeline = load_pipeline()

if pipeline:
    msg = st.text_input("Customer Message:")
    if st.button("Submit") and msg:
        with st.spinner("Processing..."):
            res = pipeline.run(msg)
            
            st.subheader("Decision: " + res["decision"])
            if res["decision"] == "ESCALATE":
                st.warning(f"Reason: {res['escalation_reason']}")
            else:
                st.success("Auto-Handled Safely")
                
            st.write("**Intent:**", res["intent"], f"(Confidence: {res['intent_confidence']:.2f})")
            st.write("**Drafted Reply:**")
            st.info(res["generated_reply"])
            st.write("**Grounded:**", res["is_grounded"])
            
            st.write("**Retrieved Evidence:**")
            for i, c in enumerate(res["retrieved_cases"]):
                st.caption(f"[{i+1}] {c['customer_message']} -> {c['support_message']} (Sim: {c.get('similarity_score', 0):.2f})")
