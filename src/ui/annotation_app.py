import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Hiver Golden Set Annotator", layout="wide")

st.title("Golden Set Human Annotation Queue")
st.markdown("According to the assignment requirements, you must hand-label 150-250 examples yourself. This tool helps you do that rapidly.")

queue_path = "data/golden_set/annotation_queue.csv"
labels_path = "data/golden_set/golden_labels.csv"

# Load Queue
if not os.path.exists(queue_path):
    st.error("Annotation queue not found. Please run the data splitting pipeline first.")
    st.stop()

@st.cache_data
def load_queue():
    return pd.read_csv(queue_path)

queue_df = load_queue()

# Load existing labels
if os.path.exists(labels_path):
    labels_df = pd.read_csv(labels_path)
    annotated_ids = set(labels_df['case_id'].astype(str))
else:
    labels_df = pd.DataFrame(columns=['case_id', 'true_intent', 'human_escalate'])
    annotated_ids = set()

total_cases = len(queue_df)
annotated_count = len(annotated_ids)

st.progress(annotated_count / total_cases)
st.write(f"**Progress:** {annotated_count} / {total_cases} cases annotated.")

if annotated_count >= total_cases:
    st.success("🎉 Golden Set annotation complete! You can now proceed to model evaluation.")
    st.stop()
elif annotated_count >= 150:
    st.info("✅ You have reached the minimum required 150 cases! You can stop here or continue.")

# Find the next unannotated case
unannotated_df = queue_df[~queue_df['case_id'].astype(str).isin(annotated_ids)]
current_case = unannotated_df.iloc[0]

st.divider()

st.subheader("Current Case")
st.markdown(f"**Case ID:** `{current_case['case_id']}`")
st.markdown(f"**Customer:** `{current_case['author_id_customer']}`")

st.info(f"🗨️ **Customer Message:**\n\n{current_case['customer_message']}")
st.success(f"🎧 **Historical Brand Reply:**\n\n{current_case['support_message']}")

st.divider()

intents = [
    "Order Status & Logistics",
    "Returns, Refunds & Cancellations",
    "Account, Billing & Prime",
    "Product Quality & Hardware",
    "Non-English Support",
    "General Inquiry & Feedback"
]

with st.form(key='annotation_form'):
    st.subheader("Annotation Details")
    
    selected_intent = st.radio("1. What is the True Intent of the customer?", options=intents)
    
    should_escalate = st.radio("2. Should this be escalated to a human agent?", 
                               options=["No (Bot can handle)", "Yes (Requires human)"],
                               help="Escalate if it involves sensitive info, complex billing, or explicit anger.")
    
    submit = st.form_submit_button("Save & Next")
    
    if submit:
        escalate_bool = True if should_escalate == "Yes (Requires human)" else False
        
        new_label = pd.DataFrame([{
            'case_id': current_case['case_id'],
            'customer_message': current_case['customer_message'],
            'support_message': current_case['support_message'],
            'true_intent': selected_intent,
            'human_escalate': escalate_bool
        }])
        
        updated_labels = pd.concat([labels_df, new_label], ignore_index=True)
        updated_labels.to_csv(labels_path, index=False)
        st.rerun()
