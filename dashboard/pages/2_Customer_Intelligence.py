
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# LOAD DATA
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

file_path = os.path.join(
    BASE_DIR,
    "data",
    "cleaned_churn.csv"
)

df = pd.read_csv(file_path)

# TITLE
st.title("👥 Customer Segmentation Analytics")

st.markdown("""
Analyze customer behavior across demographics,
financial profiles, and churn patterns.
""")

# SUNBURST CHART

st.subheader("Customer Segment Distribution")

fig = px.sunburst(
    df,
    path=[
        "Geography",
        "Gender",
        "Exited"
    ],
    values="Balance",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# AGE ANALYSIS

st.subheader("Age Group Analysis")

fig2 = px.box(
    df,
    x="Exited",
    y="Age",
    color="Exited",
    template="plotly_dark"
)

st.plotly_chart(fig2, use_container_width=True)

# PRODUCT ANALYSIS

st.subheader("Products vs Churn")

fig3 = px.histogram(
    df,
    x="NumOfProducts",
    color="Exited",
    barmode="group",
    template="plotly_dark"
)

st.plotly_chart(fig3, use_container_width=True)

# BUSINESS INSIGHTS

st.info("""
### Key Insights

• Customers with fewer products churn more frequently

• Senior customers show higher exit probability

• Germany contributes heavily to churn concentration

• Female customers show slightly higher churn trend
""")

st.warning("""
Germany shows the highest churn exposure among all regions.
""")