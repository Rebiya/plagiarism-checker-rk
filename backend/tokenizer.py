import re

def tokenize_text(text, keep_punctuation=False):
    """
    Tokenizes the input text.

    Args:
        text (str): Input text string.
        keep_punctuation (bool): If False, removes punctuation.

    Returns:
        list: List of tokens (strings)
    """
    if not keep_punctuation:
        # Remove punctuation except for spaces
        text = re.sub(r'[^\w\s]', '', text)
    # Split by whitespace
    tokens = text.split()
    return tokens


def tokenize_file(file_path, keep_punctuation=False):
    """
    Reads a file and tokenizes its content.

    Args:
        file_path (str): Path to input text file.
        keep_punctuation (bool): If False, removes punctuation.

    Returns:
        list: List of tokens
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    tokens = tokenize_text(text, keep_punctuation=keep_punctuation)
    return tokens


if __name__ == "__main__":
    FILE_PATH = "/home/rebu/Desktop/Projects/Interns/Icog labs/training-tasks/plagiarism-checker-rk/data/cleaned_data/all_cleaned.txt"  
    tokens = tokenize_file(FILE_PATH)
    print(f"Total tokens: {len(tokens)}")
    print(f"First 50 tokens: {tokens[:50]}")
