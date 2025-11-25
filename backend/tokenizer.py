import re
from typing import List


def tokenize_text(text: str) -> List[str]:
    """
    Tokenize text — assumes text is already cleaned.
    """
    return text.split()



def tokenize_file(file_path: str, keep_punctuation: bool = False) -> List[str]:
    """
    Tokenizes a text file stored on disk.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return tokenize_text(text, keep_punctuation)
