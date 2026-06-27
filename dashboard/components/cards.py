import streamlit as st

def kpi_card(title, value, icon="📊", delta=""):

    st.markdown(f"""
### {icon} {title}

# {value}

**{delta}**
""")