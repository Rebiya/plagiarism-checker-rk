import streamlit as st
import pandas as pd
import sys, os

# --------- Path Fix for backend imports ----------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.text_processing import process_uploaded_data
from backend.pipeline import plagiarism_pipeline
from backend.trie_runtime import load_trie, suggest_words


TRIE_PATH = os.path.join("data", "trie", "trie.pkl")

# =========================================================
# BASE UI
# =========================================================
st.set_page_config(
    page_title="Rabin–Karp Plagiarism Checker",
    layout="wide"
)

st.title("📚 Rabin–Karp Plagiarism Checker")

st.markdown("""
Upload a suspect document (TXT or PDF) or paste text manually.  
The system will compute similarity against reference corpus using Rabin–Karp n-gram hashing.

🟢 Plus: **Live vocabulary autocomplete from Trie**
""")


# =========================================================
# LOAD TRIE (Cached)
# =========================================================
@st.cache_resource(show_spinner=False)
def get_trie():
    return load_trie(TRIE_PATH)


trie = get_trie()

# =========================================================
# 🔍 Trie Global Search (optional)
# =========================================================
with st.expander("🔍 Search inside words"):
    q = st.text_input("Substring", key="contains_search")
    if q:
        results = []
        def scan_trie(node, path=""):
            if node.is_end_of_word and q in path:
                results.append(path)
            for c, child in node.children.items():
                scan_trie(child, path + c)
        scan_trie(trie)
        st.write(results[:25] if results else "No matches.")


# =========================================================
# 👑 SESSION STATE SETUP
# =========================================================
# user_text   = actual textarea content
# clicked_word = suggestion pill chosen
if "user_text" not in st.session_state:
    st.session_state["user_text"] = ""

if "clicked_word" not in st.session_state:
    st.session_state["clicked_word"] = None


# =========================================================
# HANDLE CLICKED SUGGESTION BEFORE RENDER
# =========================================================
if st.session_state.clicked_word:

    text = st.session_state.user_text.strip()

    # split existing text
    parts = text.split()
    if len(parts) > 0:
        parts[-1] = st.session_state.clicked_word  # replace only last
    else:
        parts = [st.session_state.clicked_word]

    st.session_state.user_text = " ".join(parts) + " "
    st.session_state.clicked_word = None
    st.rerun()


# =========================================================
# MAIN INPUT UI
# =========================================================
st.divider()
st.header("🕵️ Suspicious Document Check")

col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("Upload suspect file:", type=["txt", "pdf"])

with col2:
    user_text = st.text_area(
        "Or paste text here:",
        key="user_text",
        placeholder="Start typing...",
        height=200
    )


# =========================================================
# 🔥 REAL-TIME AUTOCOMPLETE LOGIC
# =========================================================
suggestions = []
prefix = ""

if st.session_state.user_text.strip():
    words = st.session_state.user_text.strip().split()
    prefix = words[-1]
    if prefix:
        suggestions = suggest_words(prefix, trie, max_results=8)


# =========================================================
# SUGGESTION UI — LIVE, AUTO-UPDATE
# =========================================================
if suggestions:
    clicked = st.pills(
        label="Autocomplete",
        options=suggestions,
        selection_mode="single",
        key="autocomplete_pills"
    )

    if clicked:
        st.session_state.clicked_word = clicked
        st.rerun()

# =========================================================
# PROCESS BUTTON — PLAGIARISM
# =========================================================
if st.button("Scan for Plagiarism"):
    if uploaded_file is None and not st.session_state.user_text.strip():
        st.error("⚠️ Please upload a file or paste text.")
        st.stop()

    # 1️⃣ Extract text
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1].lower()
        file_bytes = uploaded_file.read()
        raw_text = process_uploaded_data(file_bytes, file_type)
        if raw_text is None:
            st.error("Could not process file. Supported: TXT or PDF only.")
            st.stop()
    else:
        raw_text = st.session_state.user_text

    # 2️⃣ Run plagiarism
    result = plagiarism_pipeline(raw_text)

    st.success("✔ Scan complete!")

    # ---- Score ----
    st.markdown("### 📊 Similarity / Plagiarism Score")
    st.progress(int(result["score_percent"]))
    st.metric("Score (%)", f"{result['score_percent']:.2f}%")

    # ---- Clean preview ----
    with st.expander("Cleaned Text Preview"):
        st.write(result["cleaned_text"][:1000] + ("..." if len(result["cleaned_text"]) > 1000 else ""))

    # ---- Stats ----
    st.markdown("### 🔹 Statistics")
    st.write(f"Total tokens: **{result['tokens']}**")
    st.write(f"Total n-grams: **{result['ngrams_total']}**")
    st.write(f"Matched n-grams: **{result['ngrams_matched']}**")
    st.write(f"N-gram window size k: **{result['k']}**")

    # ---- Matches ----
    if result["matches"]:
        st.markdown("### 🔹 Sample Matched n-grams")
        df = pd.DataFrame(result["matches"], columns=["Hash", "Start Index"])
        st.dataframe(df.head(50))
    else:
        st.info("No matches found.")
