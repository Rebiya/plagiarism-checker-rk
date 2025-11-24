import os
import re

# Paths
INPUT_DIR = "/home/rebu/Desktop/Projects/Interns/Icog labs/training-tasks/plagiarism-checker-rk/data/AUTHORS"
OUTPUT_DIR = "/home/rebu/Desktop/Projects/Interns/Icog labs/training-tasks/plagiarism-checker-rk/data/cleaned_data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "all_cleaned.txt")

# Optional: split large files into chunks if > MAX_CHARS_PER_FILE
MAX_CHARS_PER_FILE = 1_000_000  # adjust if needed

def clean_text(text):
    # Lowercase
    text = text.lower()
    # Normalize whitespace (multiple spaces/newlines -> single space)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    all_text = []

    # Recursively process all .txt files in AUTHORS folder
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                    cleaned = clean_text(text)
                    
                    # Optionally split large files
                    if len(cleaned) > MAX_CHARS_PER_FILE:
                        for i in range(0, len(cleaned), MAX_CHARS_PER_FILE):
                            chunk = cleaned[i:i+MAX_CHARS_PER_FILE]
                            all_text.append(chunk)
                    else:
                        all_text.append(cleaned)

    # Save combined cleaned text
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(all_text))

    print(f"All cleaned text saved to {OUTPUT_FILE}")
    print(f"Total chunks/files combined: {len(all_text)}")

if __name__ == "__main__":
    main()
