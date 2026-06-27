import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path

from components.cards import kpi_card

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="FinBank Analytics",
    page_icon="🏦",
    layout="wide"
)

# ==========================================
# LOAD CSS
# ==========================================
def load_css():
    css_path = Path(__file__).parent / "assets" / "style.css"
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ==========================================
# LOAD DATA (IMPORTANT FIX)
# ==========================================
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned_churn.csv")

df = pd.read_csv(DATA_PATH)

# ==========================================
# SIDEBAR FILTERS
# ==========================================
st.sidebar.header("Dashboard Filters")

gender = st.sidebar.multiselect(
    "Gender",
    options=df["Gender"].unique(),
    default=list(df["Gender"].unique())
)

geo = st.sidebar.multiselect(
    "Geography",
    options=df["Geography"].unique(),
    default=list(df["Geography"].unique())
)

# ==========================================
# FILTER DATA (FIXED ONCE ONLY)
# ==========================================
filtered_df = df[
    (df["Gender"].isin(gender)) &
    (df["Geography"].isin(geo))
]

# ==========================================
# EMPTY DATA SAFETY (IMPORTANT FIX)
# ==========================================
if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()
# ==========================================
# BUSINESS METRICS
# ==========================================

total_customers = len(filtered_df)

churn_rate = filtered_df["Exited"].mean() * 100

total_balance = filtered_df["Balance"].sum()
avg_balance = filtered_df["Balance"].mean()

accuracy = 86.0

high_risk = filtered_df[
    (filtered_df["Age"] > 45) &
    (filtered_df["IsActiveMember"] == 0)
].shape[0]

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div style="
padding:20px;
border-radius:20px;
background:linear-gradient(135deg,#0F172A,#1E293B);
border:1px solid #334155;
">

<h1 style="
text-align:center;
font-size:42px;
color:white;
margin-bottom:10px;">

🏦 FinBank Analytics Platform

</h1>

<p style="
text-align:center;
font-size:18px;
color:#CBD5E1;">

AI Powered Banking Intelligence Dashboard

</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# KPI CARDS
# ==========================================

k1, k2, k3, k4 = st.columns(4)

with k1:
    kpi_card(
        "Customers",
        f"{total_customers:,}",
        "👥",
        "+3.4%"
    )

with k2:
    kpi_card(
        "Churn Rate",
        f"{churn_rate:.1f}%",
        "📉",
        "-1.8%"
    )

with k3:
    kpi_card(
        "Revenue",
        f"${total_balance/1_000_000:.2f}M",
        "💰",
        "+5.2%"
    )

with k4:
    kpi_card(
        "Model Accuracy",
        f"{accuracy:.1f}%",
        "🤖",
        "+0.6%"
    )

st.write("")
st.header("📊 Executive Dashboard")

col1, col2 = st.columns(2)

# ===========================
# Churn by Age
# ===========================

with col1:

    age_churn = (
        filtered_df.groupby("Age")["Exited"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        age_churn,
        x="Age",
        y="Exited",
        markers=True,
        title="Customer Churn Rate by Age"
    )

    fig.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ===========================
# Exit Distribution
# ===========================

with col2:

    exit_labels = filtered_df["Exited"].replace({
        0: "Retained",
        1: "Exited"
    })

    pie = px.pie(
        names=exit_labels,
        hole=0.65,
        title="Customer Distribution"
    )

    pie.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )
# ==========================================
# ABOUT SECTION
# ==========================================
st.markdown("---")

left, right = st.columns(2)

with left:

    geo = (
        filtered_df.groupby("Geography")
        .size()
        .reset_index(name="Customers")
    )

    fig = px.bar(
        geo,
        x="Geography",
        y="Customers",
        color="Customers",
        title="Customers by Geography"
    )

    fig.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    balance = (
        filtered_df.groupby("Geography")["Balance"]
        .sum()
        .reset_index()
    )

    fig = px.treemap(
        balance,
        path=["Geography"],
        values="Balance",
        title="Revenue Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================
# FEATURES
# ==========================================

st.markdown("## 🚀 Platform Features")

f1,f2 = st.columns(2)

with f1:

    st.markdown("""
    <div class="feature-card">
    <h3>📈 Customer Churn Analytics</h3>
    Analyze customer exit behavior across demographics,
    financial profiles, and engagement patterns.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
    <h3>🌍 Geography Risk Intelligence</h3>
    Identify churn exposure across France, Germany,
    and Spain.
    </div>
    """, unsafe_allow_html=True)

with f2:

    st.markdown("""
    <div class="feature-card">
    <h3>💰 Revenue Risk Monitoring</h3>
    Quantify revenue impact caused by high-value
    customer churn.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
    <h3>🤖 AI Churn Prediction</h3>
    Predict customer churn probability using
    machine learning models.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
st.markdown("---")
st.header("🧠 AI Business Insights")

highest = (
    filtered_df.groupby("Geography")["Exited"]
    .mean()
    .idxmax()
)

inactive = (
    filtered_df["IsActiveMember"] == 0
).sum()

one_product = (
    filtered_df["NumOfProducts"] == 1
).sum()


st.success(f"""
### Executive Summary

• Highest churn region: **{highest}**

• Inactive customers: **{inactive:,}**

• Customers with only one product: **{one_product:,}**

### Recommended Action

Focus retention campaigns on inactive customers and
single-product customers in **{highest}**.
""")

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">
Built with ❤️ using Python, Streamlit, Plotly & Machine Learning
</div>
""", unsafe_allow_html=True)