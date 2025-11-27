import re
from typing import List


def tokenize_text(text: str, keep_punctuation: bool = False) -> list:
    """
    Tokenizes text on whitespace and punctuation.
    Punctuation is removed unless keep_punctuation=True.
    """
    if not keep_punctuation:
        text = re.sub(r"[^\w\s]", " ", text)  # <-- replace punctuation with space
    return text.split()





def tokenize_file(file_path: str, keep_punctuation: bool = False) -> List[str]:
    """
    Tokenizes a text file stored on disk.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return tokenize_text(text, keep_punctuation)
