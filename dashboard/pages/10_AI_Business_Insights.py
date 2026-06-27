import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Business Insights", page_icon="🤖", layout="wide")

st.title("🤖 AI Business Insights")

# Load dataset
df = pd.read_csv("data/cleaned_churn.csv")

# ==========================
# KPIs
# ==========================

churn_rate = df["Exited"].mean() * 100
avg_age = df["Age"].mean()
avg_balance = df["Balance"].mean()
active_rate = df["IsActiveMember"].mean() * 100
avg_credit = df["CreditScore"].mean()

highest_churn = (
    df.groupby("Geography")["Exited"]
    .mean()
    .sort_values(ascending=False)
)

st.subheader("📊 Business Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Churn Rate", f"{churn_rate:.2f}%")
col2.metric("Avg Credit Score", f"{avg_credit:.0f}")
col3.metric("Avg Balance", f"${avg_balance:,.0f}")
col4.metric("Active Customers", f"{active_rate:.1f}%")

st.divider()

# ==========================
# AI Insights
# ==========================

st.subheader("🧠 AI Recommendations")

insights = []

if churn_rate > 25:
    insights.append("⚠️ Customer churn is high. Launch customer retention campaigns immediately.")
else:
    insights.append("✅ Customer churn is within a healthy range.")

if avg_age > 45:
    insights.append("👥 Most customers are older. Promote premium banking products.")

if active_rate < 60:
    insights.append("📉 Customer engagement is low. Introduce cashback and loyalty rewards.")

if avg_balance > 80000:
    insights.append("💰 Customers maintain high balances. Prioritize VIP relationship management.")

insights.append(
    f"🌍 Highest churn is observed in **{highest_churn.index[0]}**."
)

for item in insights:
    st.success(item)

st.divider()

# ==========================
# Business Actions
# ==========================

st.subheader("🎯 Recommended Business Actions")

st.info("""
✅ Launch targeted retention campaigns.

✅ Reward active customers.

✅ Offer premium banking services.

✅ Improve customer service in high-risk regions.

✅ Cross-sell insurance and loan products.

✅ Use AI to monitor churn every month.
""")

st.divider()

st.subheader("🏦 Overall AI Verdict")

if churn_rate > 20:
    st.error("Business Risk: HIGH 🔴")
elif churn_rate > 10:
    st.warning("Business Risk: MEDIUM 🟡")
else:
    st.success("Business Risk: LOW 🟢")