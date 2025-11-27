
# 📚 Plagiarism Detector + Autocomplete System

### (Trie + Rabin–Karp + WordNet Synonym Awareness)

An end-to-end system that combines **synonym-aware plagiarism detection** with a **high-performance Trie autocomplete engine**.
Supports **PDF/text uploads**, cleaning, hashing, plagiarism scoring, semantic matching, and autocomplete suggestions inside a **Streamlit UI**.

📌 [Sequence Diagram](https://drive.google.com/file/d/1lka8H2hE3M1fsx4-Pqvljg8ZQ1s4lh04/view?usp=sharing)

📌 [Use-Case Diagram](https://drive.google.com/file/d/1mIpJhoXA_cmK9TAabGXjbyIushrg9zDT/view?usp=sharing)

---

## ✨ Key Features

### 🔍 Plagiarism Detection

* Rabin–Karp hashing for substring similarity.
* **Semantic plagiarism detection via WordNet synonyms**.
* Accepts both **text input** and **PDF uploads** (Streamlit).
* Normalize & clean text for consistent matching.
* Download plagiarism result as CSV.
* **Reference hashing & vocabulary lookup**.
* CLI and Streamlit UI.

### ⚡ Trie Auto-Completion

* Prefix lookup in **O(k)** time (k = prefix length).
* Built offline → loaded at runtime.
* Streamlit **live suggestions** using callback.

### 🎯 Streamlit UI

* Upload documents.
* Compute plagiarism score.
* Live autocomplete suggestions.
* Replace last typed token when a suggestion is selected.

---

# 🧠 System Architecture

```
User (Streamlit UI)
   ├─ Text Input (typing)
   ├─ File Upload (.txt / .pdf)
   ↓
Backend Pipeline
 ├─ Text Processing
 │   ├─ Cleaning / Normalization
 │   └─ Tokenization
 ├─ Plagiarism Module (Rabin–Karp)
 │   ├─ Load Reference Hashes
 │   ├─ Compute Suspect Hashes
 │   ├─ Compare Matches
 │   └─ Score & Report
 └─ Autocomplete Module (Trie)
     ├─ Load Prebuilt Trie
     ├─ Query Prefix
     └─ Return Suggestions
```

---

# 📁 Folder Structure

```
plagiarism-checker-rk/
│
├── README.md
├── requirements.txt
│
├── app.py                     # Main Streamlit UI entry
│
├── data/
│   ├── trie/
│   │   └── trie.pkl           # Serialized Trie
│   ├── hashed/
│   │   ├── reference_hashes.pkl
│   │   └── vocab.pkl
│   ├── cleaned_data/
│   │   └── all_cleaned.txt
│   └── AUTHORS/               # Raw reference dataset
│
├── backend/
│   ├── cli.py                 # CLI interface
│   ├── hashing.py             # Rabin–Karp implementation
│   ├── plagiarism.py          # Core scoring + pipeline
│   ├── text_processing.py     # PDF/Text cleaning
│   ├── pipeline.py            # Suspect analysis orchestrator
│   ├── ref_builder.py         # Build reference corpus
│   ├── semantic_hashing.py    # WordNet synonym mapping
│   ├── tokenizer.py           # Token utilities
│   ├── trie_builder.py        # Build Trie from reference data
│   ├── trie_runtime.py        # Trie loader + suggest_words()
│   └── __init__.py
│
├── web/
│   └── app.py                 # Streamlit app interface
│
└── test/                      # pytest tests
```

---

# 🧩 Code Interaction Overview

### 1️⃣ Text Ingestion

* User uploads file (PDF / TXT) or types text.
* `process_uploaded_data()` extracts raw content.

### 2️⃣ Normalization & Cleaning

Defined in `text_processing.py`:

* Lowercase
* Remove punctuation
* Condense whitespace
* Extract text from PDF
* Tokenize

### 3️⃣ Plagiarism Detection

Rabin–Karp over n-grams:

* Compute rolling hashes
* Compare against reference hash set
* Calculate similarity score (% matched)
* Return matches + metadata

### 4️⃣ WordNet Synonym Awareness

In `semantic_hashing.py`:

* Expand tokens using WordNet synonym sets
* Hash synonym variants → detect semantic match

---

# 🧠 Synonym-Aware Matching Example

Input:

```
student writes code
```

WordNet expansion:

```
student → learner, pupil
code → program, cipher
```

Thus the system detects:

* *student writes program*
* *learner writes code*
* etc.

This improves real plagiarism detection, not just string matching.

---

# 🌲 Trie Autocomplete System

### Why Trie?

* Predictive suggestions in **O(k)** lookup.
* Memory-efficient prefix tree.
* No regex search or substring scan.

### Build Phase

Run:

```
python -m backend.trie_builder
```

Steps:

1. Load reference corpus
2. Tokenize
3. Insert into Trie
4. Serialize to `data/trie/trie.pkl`

### Runtime Phase

`trie_runtime.py`:

```python
trie = load_trie(TRIE_PATH)
suggest_words(prefix, limit=10)
```

Provides dynamic autocomplete suggestions in the Streamlit UI.

---

# 💻 Streamlit Interface

User Interactions:

* Upload PDF/text
* Live autocomplete suggestions
* Press “Check Plagiarism”
* View overall score + match positions

Mechanics:

* On text input → send prefix to Trie
* On selection → inject suggestion into input
* Plagiarism pipeline runs on submit

---

# 🧪 Testing

Uses `pytest`:

* Trie search / insertion
* PDF extraction
* Synonym detection
* Token cleaning

Run:

```
pytest -v
```

---

# 🧰 Tech Stack

| Component      | Technology     |
| -------------- | -------------- |
| UI             | Streamlit      |
| NLP            | NLTK WordNet   |
| Data Structure | Trie           |
| Algorithm      | Rabin–Karp     |
| PDF Processing | pypdf          |
| Testing        | pytest         |
| CI/CD          | GitHub Actions |

---

# ☁️ Continuous Integration

* Trigger on push / pull request
* Install deps
* Run all tests
* Fail if any test breaks

---

# 🔨 Local Setup

### 1. Clone the repo

```
git clone https://github.com/username/plagiarism-checker-rk
cd plagiarism-checker-rk
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Build Reference Dataset

```
python backend/text_processing.py
```

### 4. Build Reference Hash Index

```
python -m backend.ref_builder
```

### 5. Build Trie

```
python -m backend.trie_builder
```

### 6. Launch Streamlit UI

```
streamlit run web/app.py
```

---

# 🧭 CLI Usage (Optional)

Autocomplete:

```
python -m backend.cli "stud"
>>> ["student", "study", "studio"]
```

---

