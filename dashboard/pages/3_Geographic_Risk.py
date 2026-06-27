
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
st.title("🌍 Geography Risk Analytics")

st.markdown("""
Regional churn exposure and financial risk assessment
across European banking markets.
""")

# COUNTRY CHURN

st.subheader("Country-wise Churn Rate")

geo_churn = df.groupby(
    "Geography"
)["Exited"].mean().reset_index()

fig = px.bar(
    geo_churn,
    x="Geography",
    y="Exited",
    color="Geography",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# SCATTER ANALYSIS

st.subheader("Balance vs Age by Geography")

fig2 = px.scatter(
    df,
    x="Age",
    y="Balance",
    color="Geography",
    size="EstimatedSalary",
    template="plotly_dark"
)

st.plotly_chart(fig2, use_container_width=True)

# HEATMAP STYLE DENSITY

st.subheader("Customer Density Heatmap")

fig3 = px.density_heatmap(
    df,
    x="Age",
    y="CreditScore",
    z="Balance",
    template="plotly_dark"
)

st.plotly_chart(fig3, use_container_width=True)

# INSIGHTS

st.warning("""
### Geographic Risk Findings

• Germany shows highest churn exposure

• France has largest customer base

• Spain demonstrates moderate churn behavior

• Older customers with high balances are higher risk
""")
st.warning("""
Germany shows the highest churn exposure among all regions.
""")