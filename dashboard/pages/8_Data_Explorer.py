import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Data Explorer",
    layout="wide"
)

st.title("📊 Data Explorer")

st.markdown("""
Upload any CSV dataset and perform
interactive exploratory data analysis.
""")

# =====================================
# FILE UPLOAD
# =====================================

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # =====================================
    # DATA OVERVIEW
    # =====================================

    st.markdown("## 📄 Dataset Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Rows",
        df.shape[0]
    )

    c2.metric(
        "Columns",
        df.shape[1]
    )

    c3.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    # =====================================
    # STATISTICS
    # =====================================

    st.markdown("## 📈 Statistical Summary")

    st.dataframe(
        df.describe(),
        use_container_width=True
    )

    # =====================================
    # MISSING VALUES
    # =====================================

    st.markdown("## ⚠ Missing Values")

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing": df.isnull().sum()
    })

    st.dataframe(
        missing,
        use_container_width=True
    )

    # =====================================
    # VISUALIZATION SECTION
    # =====================================

    st.markdown("## 📊 Interactive Visualization")

    numeric_cols = df.select_dtypes(
        include=["int64","float64"]
    ).columns

    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Histogram",
            "Box Plot",
            "Scatter Plot",
            "Correlation Heatmap"
        ]
    )

    # =====================================
    # HISTOGRAM
    # =====================================

    if chart_type == "Histogram":

        col = st.selectbox(
            "Select Column",
            numeric_cols
        )

        fig = px.histogram(
            df,
            x=col,
            nbins=30,
            title=f"Distribution of {col}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================
    # BOXPLOT
    # =====================================

    elif chart_type == "Box Plot":

        col = st.selectbox(
            "Select Column",
            numeric_cols
        )

        fig = px.box(
            df,
            y=col,
            title=f"Box Plot of {col}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================
    # SCATTER
    # =====================================

    elif chart_type == "Scatter Plot":

        x_col = st.selectbox(
            "X Axis",
            numeric_cols
        )

        y_col = st.selectbox(
            "Y Axis",
            numeric_cols,
            index=1
        )

        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            title=f"{x_col} vs {y_col}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================
    # CORRELATION HEATMAP
    # =====================================

    elif chart_type == "Correlation Heatmap":

        corr = df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            title="Correlation Heatmap"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================
    # DOWNLOAD DATA
    # =====================================

    st.markdown("## ⬇ Download Dataset")

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        "cleaned_data.csv",
        "text/csv"
    )