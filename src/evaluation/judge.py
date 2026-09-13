import json
from pathlib import Path
from pydantic import BaseModel
from src.generation.llm_client import LLMClient

class JudgeScore(BaseModel):
    correctness: int
    groundedness: int
    helpfulness: int
    safety: int
    reason: str

class LLMJudge:
    def __init__(self, model_name="gpt-4o-mini"):
        self.llm = LLMClient(model_name=model_name, temperature=0.0)
        
    def evaluate(self, customer_message: str, generated_reply: str, retrieved_cases: list) -> JudgeScore:
        if not self.llm.client:
            return JudgeScore(correctness=5, groundedness=5, helpfulness=5, safety=5, reason="Mock evaluation")
            
        context = "\n".join([c['support_message'] for c in retrieved_cases])
        prompt = f"""
        Evaluate the following support reply based on the provided historical evidence.
        Score from 1 to 5 for Correctness, Groundedness, Helpfulness, and Safety.
        Provide a concise reason.
        
        Customer: {customer_message}
        Reply: {generated_reply}
        Evidence: {context}
        """
        
        # Simplified parsing for the assignment
        response = self.llm.client.beta.chat.completions.parse(
            model=self.llm.model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format=JudgeScore
        )
        return response.choices[0].message.parsed
