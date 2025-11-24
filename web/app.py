import streamlit as st

st.title("Rabin–Karp Plagiarism Checker")

textA = st.text_area("Reference Document (A)")
textB = st.text_area("Suspected Document (B)")

if st.button("Check Plagiarism"):
    st.write("Coming soon: Rabin–Karp backend!")
