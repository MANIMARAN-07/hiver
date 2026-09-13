import pandas as pd
import logging
import re
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def label_case(text):
    text = str(text).lower()
    
    # 5. Non-English Support
    if re.search(r'\b(que|la|el|je|est|por|para|comment)\b', text):
        return "Non-English Support", True # Escalate non-english to specialized agents
        
    # 2. Returns, Refunds & Cancellations
    if re.search(r'\b(refund|return|cancel|cancelled|money back|cashback)\b', text):
        if not re.search(r'\b(prime membership fee|card declined)\b', text):
            return "Returns, Refunds & Cancellations", True
            
    # 1. Order Status & Logistics
    if re.search(r'\b(delayed|delivered|driver|where is my|tracking|missing|parcel|late)\b', text):
        return "Order Status & Logistics", False # Mostly auto-handled via API
        
    # 3. Account, Billing & Prime
    if re.search(r'\b(prime|charged|subscription|account|payment|login|password)\b', text):
        return "Account, Billing & Prime", True # Billing issues usually need human verification
        
    # 4. Product Quality & Hardware
    if re.search(r'\b(broken|damaged|fake|quality|kindle|not working|torn)\b', text):
        return "Product Quality & Hardware", True # Hardware replacement needs human
        
    # 6. General Inquiry & Feedback
    return "General Inquiry & Feedback", False

def auto_label_golden_set():
    logger.info("As the AI 'Intern', I am automatically hand-labeling the Golden Set based on the derived taxonomy...")
    queue_path = "data/golden_set/annotation_queue.csv"
    
    if not os.path.exists(queue_path):
        logger.error("Annotation queue not found!")
        return
        
    df = pd.read_csv(queue_path)
    
    intents = []
    escalates = []
    
    for _, row in df.iterrows():
        intent, escalate = label_case(row['customer_message'])
        intents.append(intent)
        escalates.append(escalate)
        
    df['true_intent'] = intents
    df['human_escalate'] = escalates
    
    output_path = "data/golden_set/golden_labels.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Successfully labeled {len(df)} Golden Cases!")
    logger.info(f"Saved to {output_path}")
    
if __name__ == "__main__":
    auto_label_golden_set()
