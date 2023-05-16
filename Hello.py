import streamlit as st

st.set_page_config(
    page_title="Your Financial Assistant",
    page_icon="👋",
)

st.write("# Welcome to Your Financial Assistant! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This is a financial assistant which can answer your questions from finance knowledge to stock performance. 
    **👈 Select a demo from the sidebar** to experience our finance tutor and stock analyst now!
    
    ### What We Have?
    - **Finance Tutor:** It can help you understand any finance concept by providing you its definition and a lecture note of wikipedia.
    - **Stock Analyst:** It can analysis the performance of one stock on a given day and analysis the factors that affect stock values based on the news.
"""
)