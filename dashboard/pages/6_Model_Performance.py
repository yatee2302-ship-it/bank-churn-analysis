id="jlwm51"
import streamlit as st

st.title("📈 Model Performance")

st.metric(
    "Model Accuracy",
    "86%"
)
st.markdown("---")
st.info("""
Model used:
• Random Forest Classifier

Evaluation Metrics:
• Accuracy
• Precision
• Recall
• F1 Score
""")
st.warning("""
Germany shows the highest churn exposure among all regions.
""")