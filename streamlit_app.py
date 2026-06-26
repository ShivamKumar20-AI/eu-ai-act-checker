import streamlit as st
from classifier import classify

st.title("🇪🇺 EU AI Act Compliance Checker")
use_case = st.text_area("Describe your AI use case:")

if st.button("Check Compliance"):
    if use_case:
        result = classify(use_case)
        st.json(result)
    else:
        st.warning("Please enter a use case.")