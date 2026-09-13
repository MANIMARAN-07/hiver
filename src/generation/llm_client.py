import os
import json
from pydantic import BaseModel
from typing import List, Optional
import openai

class Claim(BaseModel):
    claim: str
    supported_by_case_ids: List[str]

class GenerationResult(BaseModel):
    reply: str
    grounded_case_ids: List[str]
    claims: List[Claim]
    confidence: float
    needs_escalation: bool
    reason: Optional[str] = None

class LLMClient:
    def __init__(self, model_name="gpt-4o-mini", temperature=0.0):
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key and self.api_key.strip() != "your-openai-api-key-here" and "actual-api-key-here" not in self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None
            
    def generate_reply(self, customer_message: str, intent: str, retrieved_cases: List[dict]) -> GenerationResult:
        if not self.client:
            msg_lower = customer_message.lower()
            
            # Simulate safety/hardware escalation
            needs_esc = False
            reason = None
            
            if any(word in msg_lower for word in ["explode", "fire", "dangerous", "sue", "lawyer", "burn"]):
                needs_esc = True
                reason = "High severity/safety issue detected."
            elif intent == "Out of Domain / Spam" or "joke" in msg_lower or "capital" in msg_lower:
                needs_esc = True
                reason = "Query is out of domain or violates support boundaries."
                
            return GenerationResult(
                reply=f"Mock response to: {customer_message}",
                grounded_case_ids=[c['case_id'] for c in retrieved_cases],
                claims=[Claim(claim="Mock claim", supported_by_case_ids=[])],
                confidence=0.8,
                needs_escalation=needs_esc,
                reason=reason
            )
            
        cases_text = "\n\n".join([f"CASE ID: {c['case_id']}\nCustomer: {c['customer_message']}\nSupport: {c['support_message']}" for c in retrieved_cases])
        
        system_prompt = f"""
You are an expert AI support agent.
Your task is to draft a reply to the customer's message.
- Be concise, helpful, and professional.
- Do NOT invent policies, refunds, or timelines.
- Ground your response ONLY in the retrieved historical cases.
- If the retrieved cases conflict or are insufficient, set needs_escalation to true and explain why.

Historical Cases Evidence:
{cases_text}
        """
        
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Customer Intent: {intent}\n\nCustomer Message: {customer_message}"}
                ],
                response_format=GenerationResult,
                temperature=self.temperature
            )
            return response.choices[0].message.parsed
        except Exception as e:
            return GenerationResult(
                reply="",
                grounded_case_ids=[],
                claims=[],
                confidence=0.0,
                needs_escalation=True,
                reason=f"LLM Generation Failed: {str(e)}"
            )
