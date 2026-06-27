
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
st.title("💰 High Value Customer Analysis")

st.markdown("""
Monitor premium customers, revenue exposure,
and financial churn risk.
""")

# FILTER HIGH VALUE CUSTOMERS

high_value = df[
    df["Balance"] > 100000
]

# KPIs

col1, col2 = st.columns(2)

col1.metric(
    "High Value Customers",
    len(high_value)
)

revenue_risk = high_value[
    high_value["Exited"] == 1
]["Balance"].sum()

col2.metric(
    "Revenue at Risk",
    f"${round(revenue_risk,2)}"
)

# BALANCE DISTRIBUTION

st.subheader("High Value Balance Distribution")

fig = px.histogram(
    high_value,
    x="Balance",
    color="Exited",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# SALARY ANALYSIS

st.subheader("Salary vs Balance")

fig2 = px.scatter(
    high_value,
    x="EstimatedSalary",
    y="Balance",
    color="Exited",
    template="plotly_dark"
)

st.plotly_chart(fig2, use_container_width=True)

# TENURE ANALYSIS

st.subheader("Tenure Analysis")

fig3 = px.box(
    high_value,
    x="Exited",
    y="Tenure",
    color="Exited",
    template="plotly_dark"
)

st.plotly_chart(fig3, use_container_width=True)

# INSIGHTS

st.error("""
### Revenue Risk Insights

• Premium customers contribute major revenue exposure

• High-balance churners create significant financial loss

• Inactive premium customers are high-risk segments

• Long-tenure customers still show churn vulnerability
""")
st.warning("""
Germany shows the highest churn exposure among all regions.
""")
