import os
import re
from typing import Optional
from io import BytesIO
from pypdf import PdfReader


# -------------------------
# TEXT CLEANING HELPERS
# -------------------------
def clean_text(raw_text: str, keep_punctuation=False) -> str:
    """
    Basic preprocessing:
    - lowercase
    - remove punctuation (optional)
    - normalize whitespace
    """
    text = raw_text.lower()

    if not keep_punctuation:
        text = re.sub(r"[^\w\s]", "", text)

    text = re.sub(r"\s+", " ", text).strip()
    return text


# -------------------------
# PDF UTILS
# -------------------------
def extract_pdf_text(uploaded_bytes: BytesIO) -> str:
    reader = PdfReader(uploaded_bytes)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


# -------------------------
# HANDLE STREAMLIT UPLOAD
# -------------------------
def process_uploaded_data(file_bytes: bytes, file_type: str, keep_punctuation=False) -> Optional[str]:
    """
    Handles uploaded file input from Streamlit.
    
    file_type: "txt" | "pdf"
    Returns cleaned text.
    """
    if file_type == "txt":
        raw = file_bytes.decode("utf-8", errors="ignore")
        return clean_text(raw, keep_punctuation)

    if file_type == "pdf":
        pdf_text = extract_pdf_text(BytesIO(file_bytes))
        return clean_text(pdf_text, keep_punctuation)

    return None


# -------------------------
# KAGGLE REFERENCE DATA
# -------------------------
def process_reference_data(input_dir: str, output_file: str, keep_punctuation=False):
    """
    - Iterates through ALL files under Kaggle dataset folder
    - Reads text or PDF
    - Cleans content
    - Writes everything into a single combined file
    """
    combined = []

    for root, _, files in os.walk(input_dir):
        for file in files:

            file_path = os.path.join(root, file)
            ext = file.lower().split(".")[-1]

            try:
                if ext == "txt":
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = clean_text(f.read(), keep_punctuation)
                        combined.append(text)

                elif ext == "pdf":
                    with open(file_path, "rb") as f:
                        raw = extract_pdf_text(f)
                        combined.append(clean_text(raw, keep_punctuation))

            except Exception as e:
                print(f"[WARN] Skipping {file_path}: {e}")

    # Save merged reference data
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("\n".join(combined))

    print(f"Reference data created → {output_file}")


# -------------------------
# TOKENIZATION
# -------------------------
def tokenize(text: str) -> list:
    return text.split()


if __name__ == "__main__":
    INPUT_DIR = "/home/rebu/Desktop/Projects/Interns/Icog labs/training-tasks/plagiarism-checker-rk/data/AUTHORS"
    OUTPUT_DIR = "/home/rebu/Desktop/Projects/Interns/Icog labs/training-tasks/plagiarism-checker-rk/data/cleaned_data"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    OUTPUT_FILE = os.path.join(OUTPUT_DIR, "all_cleaned.txt")

    # Build the Kaggle reference dataset
    process_reference_data(INPUT_DIR, OUTPUT_FILE)

    with open(OUTPUT_FILE, "r") as f:
        sample = f.read()[:200]
        print("Sample reference text:", sample)
