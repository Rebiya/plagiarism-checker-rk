import pytest
from unittest.mock import Mock, patch, mock_open
from io import BytesIO

from backend.text_processing import (
    clean_text,
    extract_pdf_text,
    process_uploaded_data,
    process_reference_data,
)

# --------------------------
# clean_text TESTS
# --------------------------
def test_clean_text_basic():
    assert clean_text("Hello WORLD") == "hello world"


def test_clean_text_remove_punct():
    assert clean_text("Hello, world!!!") == "hello world"


def test_clean_text_keep_punct():
    assert clean_text("Hello, world!", keep_punctuation=True) == "hello, world!"


def test_clean_text_whitespace_norm():
    assert clean_text(" Hello   world \n Test ") == "hello world test"


# --------------------------
# PDF EXTRACT TEXT
# --------------------------
def test_extract_pdf_text():
    """
    MOCK PdfReader so no real PDF is needed.
    """
    mock_page1 = Mock()
    mock_page1.extract_text.return_value = "Page one text"

    mock_page2 = Mock()
    mock_page2.extract_text.return_value = "Second page"

    mock_reader = Mock()
    mock_reader.pages = [mock_page1, mock_page2]

    with patch("backend.text_processing.PdfReader", return_value=mock_reader):
        out = extract_pdf_text(BytesIO(b"fake_pdf"))
        assert out == "Page one text\nSecond page"


def test_extract_pdf_text_handle_empty_pages():
    mock_page = Mock()
    mock_page.extract_text.return_value = None

    mock_reader = Mock()
    mock_reader.pages = [mock_page]

    with patch("backend.text_processing.PdfReader", return_value=mock_reader):
        out = extract_pdf_text(BytesIO(b"fake"))
        assert out == ""


# --------------------------
# process_uploaded_data
# --------------------------
def test_process_uploaded_txt():
    raw_data = b"Hello, WORLD!!"
    out = process_uploaded_data(raw_data, "txt")
    assert out == "hello world"


def test_process_uploaded_pdf():
    mock_page = Mock()
    mock_page.extract_text.return_value = "PDF text here"

    mock_reader = Mock()
    mock_reader.pages = [mock_page]

    with patch("backend.text_processing.PdfReader", return_value=mock_reader):
        out = process_uploaded_data(b"blob", "pdf")
        assert out == "pdf text here"


def test_process_uploaded_invalid_type():
    assert process_uploaded_data(b"123", "exe") is None


# --------------------------
# process_reference_data
# --------------------------
def test_process_reference_data(tmp_path):
    """
    Simulate a directory with files.
    We mock clean_text + extract_pdf_text.
    """
    # create fake text file
    txt_file = tmp_path / "file1.txt"
    txt_file.write_text("Hello world")

    pdf_file = tmp_path / "file2.pdf"
    pdf_file.write_bytes(b"%PDF!")

    out_path = tmp_path / "combined.txt"

    with patch("backend.text_processing.clean_text") as mock_clean, \
         patch("backend.text_processing.extract_pdf_text") as mock_pdf:

        mock_clean.side_effect = lambda x, *_: x.lower()
        mock_pdf.return_value = "PDF DATA"

        process_reference_data(str(tmp_path), str(out_path))

    combined = out_path.read_text()
    assert "hello world" in combined
    assert "pdf data" in combined.lower()
