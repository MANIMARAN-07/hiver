import uuid
from typing import Dict, Any
from src.intent.classifier import SemanticClassifier
from src.retrieval.faiss_index import CaseRetriever
from src.generation.llm_client import LLMClient
from src.evaluation.grounding import verify_grounding
from src.escalation.policy import EscalationPolicy

class SupportAgentPipeline:
    def __init__(self, model_dir: str, retrieval_dir: str, config: dict):
        self.config = config
        
        # Load Classifier
        self.classifier = SemanticClassifier(config["modeling"]["embedding_model"])
        self.classifier.load(f"{model_dir}/semantic_classifier.pkl")
        
        # Load Retriever
        self.retriever = CaseRetriever(config["modeling"]["embedding_model"])
        self.retriever.load(f"{retrieval_dir}/case_index")
        
        # Init Generation
        self.llm = LLMClient(model_name=config["generation"]["model"])
        
        # Init Escalation Policy
        self.policy = EscalationPolicy()
        
    def run(self, customer_message: str) -> Dict[str, Any]:
        trace_id = str(uuid.uuid4())
        
        # 1. Intent Classification
        intents = self.classifier.clf.classes_
        probs = self.classifier.predict_proba([customer_message])[0]
        max_idx = probs.argmax()
        intent = intents[max_idx]
        confidence = probs[max_idx]
        
        # 2. Retrieval
        k = self.config["modeling"]["retrieval_k"]
        retrieved_cases = self.retriever.retrieve(customer_message, k=k)
        
        # 3. Generation
        gen_result = self.llm.generate_reply(customer_message, intent, retrieved_cases)
        
        # 4. Grounding Check
        is_grounded = verify_grounding(gen_result.reply, retrieved_cases)
        
        # 5. Escalation Decision
        decision, reason = self.policy.evaluate(
            intent_confidence=confidence,
            retrieved_cases=retrieved_cases,
            llm_escalation_flag=gen_result.needs_escalation,
            is_grounded=is_grounded,
            llm_reason=gen_result.reason
        )
        
        return {
            "trace_id": trace_id,
            "intent": intent,
            "intent_confidence": float(confidence),
            "retrieved_cases": retrieved_cases,
            "generated_reply": gen_result.reply,
            "is_grounded": is_grounded,
            "decision": decision,
            "escalation_reason": reason
        }
