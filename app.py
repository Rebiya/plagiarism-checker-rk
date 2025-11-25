import streamlit as st

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from backend.text_processing import process_uploaded_data, clean_text

from backend.tokenizer import tokenize_text

st.set_page_config(page_title="Rabin–Karp Plagiarism Checker")

st.title("📚 Rabin–Karp Plagiarism Checker (Suspect File Only)")

uploaded_file = st.file_uploader(
    "Upload suspect document",
    type=["txt", "pdf"]
)

input_text = st.text_area(
    "Or paste text manually",
    placeholder="Paste suspected text here..."
)

st.write("---")

if st.button("Process Suspect Text"):
    if uploaded_file is None and not input_text.strip():
        st.error("⚠️ Please upload a file or paste text.")
        st.stop()

    # 1️⃣ If user uploaded PDF or TXT
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1].lower()
        file_bytes = uploaded_file.read()

        cleaned = process_uploaded_data(file_bytes, file_type)

        if cleaned is None:
            st.error("Could not process file. Supported: txt, pdf")
            st.stop()

    # 2️⃣ If user pasted text
    else:
        cleaned = clean_text(input_text)

    # Tokenize cleaned text
    tokens = tokenize_text(cleaned)

    st.success("✔ Suspect text processed!")
    st.write(f"Total tokens: **{len(tokens)}**")
    st.write(tokens[:50])  # preview
