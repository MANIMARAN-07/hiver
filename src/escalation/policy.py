class EscalationPolicy:
    def __init__(self, confidence_threshold=0.4, similarity_threshold=0.3):
        self.confidence_threshold = confidence_threshold
        self.similarity_threshold = similarity_threshold
        
    def evaluate(self, 
                 intent_confidence: float, 
                 retrieved_cases: list, 
                 llm_escalation_flag: bool, 
                 is_grounded: bool,
                 llm_reason: str = None) -> tuple[str, str]:
        """
        Returns (Decision, Reason)
        Decision is either 'AUTO_HANDLE' or 'ESCALATE'
        """
        if not is_grounded:
            return "ESCALATE", "Ungrounded LLM claims detected."
            
        if llm_escalation_flag:
            return "ESCALATE", llm_reason if llm_reason else "LLM determined evidence is insufficient or contradictory."
            
        if intent_confidence < self.confidence_threshold:
            return "ESCALATE", f"Intent confidence ({intent_confidence:.2f}) below threshold."
            
        if not retrieved_cases:
            return "ESCALATE", "No historical cases found to ground response."
            
        top_sim = retrieved_cases[0].get('similarity_score', 0)
        if top_sim < self.similarity_threshold:
            return "ESCALATE", f"Top retrieval similarity ({top_sim:.2f}) below threshold."
            
        return "AUTO_HANDLE", "All safety and evidence checks passed."
