import streamlit as st
import pandas as pd

st.set_page_config(page_title="Executive Report", page_icon="📑", layout="wide")

st.title("📑 Executive Report")

# Load dataset
df = pd.read_csv("data/cleaned_churn.csv")

# ==========================
# KPIs
# ==========================

customers = len(df)
churned = df["Exited"].sum()
retained = customers - churned

churn_rate = (churned / customers) * 100
avg_credit = df["CreditScore"].mean()
avg_balance = df["Balance"].mean()
avg_salary = df["EstimatedSalary"].mean()

# ==========================
# Dashboard KPIs
# ==========================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Customers", f"{customers:,}")
col2.metric("Retained", f"{retained:,}")
col3.metric("Churn Rate", f"{churn_rate:.2f}%")
col4.metric("Avg Credit", f"{avg_credit:.0f}")

st.divider()

# ==========================
# Executive Summary
# ==========================

st.subheader("📋 Executive Summary")

st.write(f"""
### Key Performance Indicators

- **Total Customers:** {customers:,}

- **Customers Retained:** {retained:,}

- **Customers Lost:** {churned:,}

- **Overall Churn Rate:** {churn_rate:.2f}%

- **Average Credit Score:** {avg_credit:.0f}

- **Average Balance:** ${avg_balance:,.2f}

- **Average Estimated Salary:** ${avg_salary:,.2f}
""")

st.divider()

# ==========================
# Management Summary
# ==========================

st.subheader("📈 Management Summary")

if churn_rate > 20:
    st.error("""
High churn has been detected.

Management should prioritize:

• Customer retention

• Loyalty programs

• Personalized banking offers

• Improved customer support
""")

else:
    st.success("""
Customer retention is healthy.

Focus on:

• Cross-selling financial products

• Growing premium customer accounts

• Increasing customer lifetime value
""")

st.divider()

# ==========================
# CEO Recommendations
# ==========================

st.subheader("💼 CEO Recommendations")

st.write("""
✅ Increase customer engagement.

✅ Reward loyal customers.

✅ Improve banking services in high-risk regions.

✅ Promote digital banking.

✅ Offer personalized loans and insurance.

✅ Continue AI-driven churn monitoring.
""")

st.divider()

# ==========================
# Download Report
# ==========================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Executive Report",
    data=csv,
    file_name="Executive_Report.csv",
    mime="text/csv"
)