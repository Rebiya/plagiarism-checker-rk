import streamlit as st
import pandas as pd
import time
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.text_processing import process_uploaded_data
from backend.pipeline import plagiarism_pipeline
from backend.trie_runtime import load_trie, suggest_words

TRIE_PATH = os.path.join("data", "trie", "trie.pkl")

st.set_page_config(
    page_title="Rabin–Karp Plagiarism Checker",
    layout="wide"
)


# =========================================================
# 1️⃣ LOAD TRIE WITH CACHE
# =========================================================
@st.cache_resource(show_spinner=False)
def get_trie():
    return load_trie(TRIE_PATH)


trie = get_trie()


# =========================================================
# 2️⃣ STREAMLIT UI
# =========================================================
st.title("📚 Rabin–Karp Plagiarism Checker")

st.markdown("""
Upload a suspect document (TXT or PDF) or paste text manually.  
The system will compute similarity against reference corpus using Rabin–Karp n-gram hashing.

---

### 🧠 🔍 Word Autocomplete (Trie + Cleaned Reference Corpus)

Type a word prefix to see **streaming autocompletion suggestions** from the reference corpus.
""")

# -------------------------
# AUTOCOMPLETE INPUT
# -------------------------
prefix = st.text_input(
    "Start typing a word to autocomplete:",
    placeholder="Type here, e.g., 'clean', 'claim', 'machine'...",
    key="autocomplete_input",
)

# ------------- debounce timer -----------------
time.sleep(0.13)   # 🔥 small debounce (130 ms) prevents spam reruns

suggestions = []
if prefix.strip():
    suggestions = suggest_words(prefix.strip(), trie, max_results=5)


# =========================================================
# 3️⃣ SHOW SUGGESTIONS AS PILLS
# =========================================================
if suggestions:
    st.markdown("#### 🔗 Suggestions")
    selected = st.pills(
        label="Autocomplete",
        options=suggestions,
        selection_mode="single",
        key="trie_suggestions",
        help="Click to auto-complete the text box.",
    )

    if selected:
        # Override text input value with clicked suggestion
        st.session_state["autocomplete_input"] = selected


# =========================================================
# 4️⃣ SEARCH INSIDE TRIE WORDS (optional)
# =========================================================
with st.expander("🔍 Search inside words (contains)"):
    search_query = st.text_input(
        "Search substring inside dictionary words:",
        placeholder="Example: 'ing'",
        key="global_search"
    )
    if search_query:
        # naive search — you can optimize later
        results = []
        def scan_trie(node, path=""):
            if node.is_end_of_word and search_query in path:
                results.append(path)
            for c, child in node.children.items():
                scan_trie(child, path + c)
        scan_trie(trie)

        st.write(results[:25] if results else "No matches found.")


# =========================================================
# 5️⃣ ORIGINAL PLAGIARISM CHECK UI (UNCHANGED)
# =========================================================
st.divider()
st.header("🕵️ Suspicious Document Check")

col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("Upload suspect file:", type=["txt", "pdf"])
    
with col2:
    input_text = st.text_area(
        "Or paste text here:",
        placeholder="Paste suspected text..."
    )


# -------------------------
# PROCESS
# -------------------------
if st.button("Scan for Plagiarism"):
    if uploaded_file is None and not input_text.strip():
        st.error("⚠️ Please upload a file or paste text.")
        st.stop()

    # 1️⃣ Get raw text
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1].lower()
        file_bytes = uploaded_file.read()
        raw_text = process_uploaded_data(file_bytes, file_type)
        if raw_text is None:
            st.error("Could not process file. Supported: TXT or PDF only.")
            st.stop()
    else:
        raw_text = input_text

    # 2️⃣ Run full pipeline
    result = plagiarism_pipeline(raw_text)

    # -------------------------
    # DISPLAY RESULTS
    # -------------------------
    st.success("✔ Suspect text scanned successfully!")

    # 3️⃣ Plagiarism Score
    st.markdown("### 📊 Similarity / Plagiarism Score")
    st.progress(int(result["score_percent"]))
    st.metric("Score (%)", f"{result['score_percent']:.2f}%")
    
    # 4️⃣ Cleaned Text Preview
    with st.expander("Preview of cleaned text"):
        st.write(result["cleaned_text"][:1000] + ("..." if len(result["cleaned_text"]) > 1000 else ""))

    # 5️⃣ Token & n-gram stats
    st.markdown("### 🔹 Statistics")
    st.write(f"Total tokens: **{result['tokens']}**")
    st.write(f"Total n-grams: **{result['ngrams_total']}**")
    st.write(f"Matched n-grams: **{result['ngrams_matched']}**")
    st.write(f"N-gram window size k: **{result['k']}**")

    # 6️⃣ Show matches in a table (hash, start_index)
    if result["matches"]:
        st.markdown("### 🔹 Sample matched n-grams")
        df_matches = pd.DataFrame(result["matches"], columns=["Hash", "Start Index"])
        st.dataframe(df_matches.head(50))  # show first 50 matches
    else:
        st.info("No matches found in reference corpus.")

