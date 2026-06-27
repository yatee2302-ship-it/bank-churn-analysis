import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os

st.set_page_config(
    page_title="AI Dataset Analysis",
    layout="wide"
)

st.title("📊 Data Upload & AI Analysis")

# ---------------- LOAD MODEL ----------------

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

# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload Customer Dataset",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # =====================================
    # DATA PREVIEW
    # =====================================

    st.header("📋 Dataset Preview")

    st.dataframe(df.head())

    # =====================================
    # DATASET SUMMARY
    # =====================================

    st.header("📈 Dataset Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Rows",
            df.shape[0]
        )

    with col2:
        st.metric(
            "Columns",
            df.shape[1]
        )

    with col3:
        st.metric(
            "Missing Values",
            df.isnull().sum().sum()
        )

    # =====================================
    # COLUMN INFORMATION
    # =====================================

    st.header("🧾 Column Information")

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Datatype": df.dtypes.astype(str)
    })

    st.dataframe(column_info)

    # =====================================
    # MISSING VALUES
    # =====================================

    st.header("⚠ Missing Values")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum()
    })

    st.dataframe(missing_df)

    # =====================================
    # NUMERIC ANALYSIS
    # =====================================

    st.header("📊 Feature Analysis")

    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    if len(numeric_cols) > 0:

        selected_col = st.selectbox(
            "Select Numeric Feature",
            numeric_cols
        )

        fig = px.histogram(
            df,
            x=selected_col,
            nbins=25,
            title=f"{selected_col} Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================
    # CORRELATION HEATMAP
    # =====================================

    if len(numeric_cols) > 1:

        st.header("🔥 Correlation Heatmap")

        corr = df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            aspect="auto"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================
    # BATCH PREDICTION
    # =====================================

    st.header("🤖 Batch Churn Prediction")

    required_columns = [
        "CreditScore",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if len(missing_columns) > 0:

        st.error(
            f"Required columns missing: {missing_columns}"
        )

    else:

        features = df[required_columns]

        predictions = model.predict(
            features
        )

        probabilities = model.predict_proba(
            features
        )[:, 1]

        df["Prediction"] = predictions

        df["Churn Probability (%)"] = (
            probabilities * 100
        ).round(2)

        st.success(
            "Predictions Generated Successfully"
        )

        st.dataframe(
            df.head()
        )

        # =====================================
        # AI INSIGHTS
        # =====================================

        st.header("💡 AI Insights")

        high_risk = df[
            df["Churn Probability (%)"] > 70
        ]

        st.metric(
            "High Risk Customers",
            len(high_risk)
        )

        st.metric(
            "Average Churn Probability",
            round(
                df[
                    "Churn Probability (%)"
                ].mean(),
                2
            )
        )

        if "Age" in df.columns:

            avg_age = round(
                high_risk["Age"].mean(),
                1
            )

            st.info(
                f"High-risk customers average age: {avg_age}"
            )

        # =====================================
        # RISK DISTRIBUTION
        # =====================================

        st.header("🚨 Risk Distribution")

        fig = px.histogram(
            df,
            x="Churn Probability (%)",
            nbins=20
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =====================================
        # DOWNLOAD RESULTS
        # =====================================

        st.header("⬇ Download Results")

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            label="Download Prediction Results",
            data=csv,
            file_name="churn_predictions.csv",
            mime="text/csv"
        )