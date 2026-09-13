from typing import List, Dict

def verify_grounding(reply: str, retrieved_cases: List[Dict]) -> bool:
    """
    Very basic grounding check.
    In a full production environment, this could involve a smaller LLM or NLI model 
    to check if 'reply' entails facts not present in 'retrieved_cases'.
    For now, if there are no retrieved cases but the reply is long, we flag it.
    """
    if not retrieved_cases and len(reply) > 50:
        return False
        
    # If the reply mentions a specific refund amount or link not in the cases, it's a hallucination.
    # We do simple heuristic checks.
    if "$" in reply or "http" in reply:
        case_texts = " ".join([c['support_message'] for c in retrieved_cases])
        if "$" in reply and "$" not in case_texts:
            return False
        if "http" in reply and "http" not in case_texts:
            return False
            
    return True
