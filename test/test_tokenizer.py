import pytest
from unittest.mock import mock_open, patch

from backend.tokenizer import tokenize_text, tokenize_file


# --------------------------
# tokenize_text
# --------------------------
def test_tokenize_text_basic():
    assert tokenize_text("hello world") == ["hello", "world"]


def test_tokenize_text_remove_punctuation():
    assert tokenize_text("hello,world!!") == ["hello", "world"]


def test_tokenize_text_keep_punct():
    assert tokenize_text("hello,world!", keep_punctuation=True) == ["hello,world!"]


def test_tokenize_text_empty():
    assert tokenize_text("") == []


# --------------------------
# tokenize_file
# --------------------------
def test_tokenize_file():
    fake = "hello world test"

    with patch("builtins.open", mock_open(read_data=fake)):
        result = tokenize_file("/fake/path.txt")

    assert result == ["hello", "world", "test"]


def test_tokenize_file_keep_punct():
    fake = "hello,world!"

    with patch("builtins.open", mock_open(read_data=fake)):
        result = tokenize_file("/path/file", keep_punctuation=True)

    assert result == ["hello,world!"]
