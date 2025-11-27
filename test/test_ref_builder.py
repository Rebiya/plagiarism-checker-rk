import builtins
import pytest
from backend import ac
from backend import tokenizer
from backend import plagiarism

def test_ref_builder_main(monkeypatch, tmp_path):
    # Create a fake cleaned file
    fake_file = tmp_path / "cleaned.txt"
    fake_file.write_text("hello world hello icog")

    # Patch tokenizer.tokenize_file to read our tmp file
    monkeypatch.setattr(tokenizer, "tokenize_file", lambda path: ["hello", "world", "hello", "icog"])

    # Patch plagiarism.build_reference_from_tokens to avoid real hashing and saving
    monkeypatch.setattr(plagiarism, "build_reference_from_tokens", lambda tokens, k=10: ({1, 2}, {"hello": 1, "world": 2, "icog": 3}))

    # Patch sys.argv
    monkeypatch.setattr("sys.argv", ["run_build_reference.py", "--input", str(fake_file)])

    # Run main
    ac.main()  # Should complete without exceptions
