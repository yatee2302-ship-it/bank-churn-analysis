
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

file_path = os.path.join(
    BASE_DIR,
    "data",
    "cleaned_churn.csv"
)

df = pd.read_csv(file_path)

st.title("📊 Banking Overview Dashboard")

# KPI SECTION

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    len(df)
)

col2.metric(
    "Churn Rate",
    f"{round(df['Exited'].mean()*100,2)}%"
)

col3.metric(
    "Active Members",
    df["IsActiveMember"].sum()
)

col4.metric(
    "Average Balance",
    f"${round(df['Balance'].mean(),2)}"
)

# CHURN DISTRIBUTION

st.subheader("Customer Churn Distribution")

fig = px.histogram(
    df,
    x="Age",
    color="Exited",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# CREDIT SCORE ANALYSIS

st.subheader("Credit Score Analysis")

fig2 = px.box(
    df,
    x="Exited",
    y="CreditScore",
    color="Exited",
    template="plotly_dark"
)

st.plotly_chart(fig2, use_container_width=True)
st.warning("""
Germany shows the highest churn exposure among all regions.
""")
