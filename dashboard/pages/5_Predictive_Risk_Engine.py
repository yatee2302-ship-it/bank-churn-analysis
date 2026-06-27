import streamlit as st
import pandas as pd
import joblib
import os
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Predictive Risk Engine",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Predictive Risk Engine")
st.markdown(
    "AI-powered customer churn prediction and risk assessment"
)

# ==========================================
# LOAD MODEL
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

model_path = os.path.join(
    BASE_DIR,
    "models",
    "churn_model.pkl"
)

model = joblib.load(model_path)

# ==========================================
# INPUT SECTION
# ==========================================

st.markdown("## 📝 Customer Information")

col1, col2 = st.columns(2)

with col1:

    credit = st.slider(
        "Credit Score",
        300,
        900,
        650
    )

    age = st.slider(
        "Age",
        18,
        90,
        40
    )

    tenure = st.slider(
        "Tenure",
        0,
        10,
        5
    )

    balance = st.number_input(
        "Account Balance",
        value=50000.0
    )

with col2:

    products = st.selectbox(
        "Number of Products",
        [1, 2, 3, 4]
    )

    card = st.selectbox(
        "Has Credit Card",
        [0, 1]
    )

    active = st.selectbox(
        "Active Member",
        [0, 1]
    )

    salary = st.number_input(
        "Estimated Salary",
        value=50000.0
    )

# ==========================================
# PREDICTION BUTTON
# ==========================================

if st.button("🚀 Predict Churn Risk"):

    input_df = pd.DataFrame({
        "CreditScore": [credit],
        "Age": [age],
        "Tenure": [tenure],
        "Balance": [balance],
        "NumOfProducts": [products],
        "HasCrCard": [card],
        "IsActiveMember": [active],
        "EstimatedSalary": [salary]
    })

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(
        input_df
    )[0][1]

    risk_score = round(
        probability * 100,
        2
    )

    st.markdown("---")

    # ==========================================
    # RISK GAUGE
    # ==========================================

    st.markdown("## 📊 Churn Risk Score")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={
                "text": "Customer Churn Risk (%)"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "steps": [
                    {
                        "range": [0, 30],
                        "color": "lightgreen"
                    },
                    {
                        "range": [30, 70],
                        "color": "gold"
                    },
                    {
                        "range": [70, 100],
                        "color": "salmon"
                    }
                ]
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================================
    # CUSTOMER PROFILE
    # ==========================================

    st.markdown("## 📋 Customer Profile")

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.metric(
            "Age",
            age
        )

    with p2:
        st.metric(
            "Balance",
            f"${balance:,.0f}"
        )

    with p3:
        st.metric(
            "Products",
            products
        )

    with p4:
        st.metric(
            "Salary",
            f"${salary:,.0f}"
        )

    # ==========================================
    # RISK ASSESSMENT
    # ==========================================

    st.markdown("## 🔍 Risk Assessment")

    risk_factors = []

    if age > 50:
        risk_factors.append(
            "Older customer segment"
        )

    if balance > 100000:
        risk_factors.append(
            "High account balance"
        )

    if active == 0:
        risk_factors.append(
            "Inactive member"
        )

    if products == 1:
        risk_factors.append(
            "Low product engagement"
        )

    if len(risk_factors) > 0:

        for factor in risk_factors:
            st.warning(
                f"⚠ {factor}"
            )

    else:

        st.success(
            "No major risk indicators detected."
        )

    # ==========================================
    # FINAL RESULT
    # ==========================================

    st.markdown("## 🎯 Prediction Result")

    if prediction == 1:

        st.error(
            f"🔴 HIGH CHURN RISK ({risk_score}%)"
        )

        st.markdown(
            "### 💡 Recommended Retention Actions"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.info(
                "🎁 Loyalty Incentive"
            )

        with c2:
            st.info(
                "📞 Relationship Outreach"
            )

        with c3:
            st.info(
                "💳 Premium Product Offer"
            )

    else:

        st.success(
            f"🟢 LOW CHURN RISK ({risk_score}%)"
        )

        st.markdown(
            "### 💡 Recommended Actions"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.info(
                "😊 Maintain Engagement"
            )

        with c2:
            st.info(
                "📧 Personalized Offers"
            )

        with c3:
            st.info(
                "⭐ Reward Program"
            )

    # ==========================================
    # INPUT DATA REVIEW
    # ==========================================

    st.markdown("---")
    st.markdown("## 📄 Model Input Data")

    st.dataframe(
        input_df,
        use_container_width=True
    )