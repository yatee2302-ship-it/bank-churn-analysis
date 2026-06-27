import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Customer Segmentation",
    layout="wide"
)

st.title("👥 Customer Segmentation")

uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    required = [
        "CreditScore",
        "Age",
        "Balance",
        "EstimatedSalary"
    ]

    if all(col in df.columns for col in required):

        X = df[required]

        kmeans = KMeans(
            n_clusters=4,
            random_state=42,
            n_init=10
        )

        df["Cluster"] = kmeans.fit_predict(X)

        st.success(
            "Customer Segmentation Completed"
        )

        fig = px.scatter(
            df,
            x="Balance",
            y="EstimatedSalary",
            color="Cluster",
            hover_data=["Age"],
            title="Customer Segments"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("## Segment Summary")

        summary = df.groupby(
            "Cluster"
        )[required].mean()

        st.dataframe(
            summary,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Segmented Dataset",
            csv,
            "segmented_customers.csv",
            "text/csv"
        )

    else:

        st.error(
            "Dataset missing required columns."
        )