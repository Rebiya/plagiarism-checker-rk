import os
import pytest
from backend import plagiarism
from backend import hashing


def test_build_reference_from_tokens(tmp_path):
    tokens = ["hello", "world", "hello", "icog"]

    hash_path = tmp_path / "h.pkl"
    vocab_path = tmp_path / "v.pkl"

    hash_set, vocab = plagiarism.build_reference_from_tokens(
        tokens,
        k=2,
        out_hash_path=str(hash_path),
        out_vocab_path=str(vocab_path)
    )

    # IDs deterministically based on first appearance
    assert vocab == {"hello": 1, "world": 2, "icog": 3}

    # rolling ngrams:
    # ["hello","world"] → (1,2)
    # ["world","hello"] → (2,1)
    # ["hello","icog"] → (1,3)
    assert len(hash_set) == 3

    assert hash_path.exists()
    assert vocab_path.exists()


def test_compute_suspect_hashes_only_reference_words():
    ref_tokens = ["hello", "world", "icog"]
    vocab = hashing.word_ids(ref_tokens)

    sus_tokens = ["hello", "unknown", "world"]
    hashes = plagiarism.compute_suspect_hashes(sus_tokens, vocab, k=2)

    # unknown discarded, ids become [1,2]
    assert len(hashes) == 1
    hash_val, idx = hashes[0]
    assert idx == 0


def test_compare_hashes():
    sus = [(10,0),(20,1),(30,2)]
    ref = {10,30}

    matched, total, pairs = plagiarism.compare_hashes(sus, ref)

    assert matched == 2
    assert total == 3
    assert pairs == [(10,0),(30,2)]


def test_compute_plagiarism_score():
    assert plagiarism.compute_plagiarism_score(5,10) == 50.0
    assert plagiarism.compute_plagiarism_score(0,10) == 0.0
    assert plagiarism.compute_plagiarism_score(1,0) == 0.0


def test_scan_suspect_full_pipeline(tmp_path, monkeypatch):
    tokens = ["hello", "world", "hello", "icog"]
    k = 2

    ref_hashes, vocab = plagiarism.build_reference_from_tokens(tokens, k=k)

    def fake_loader():
        return ref_hashes, vocab

    monkeypatch.setattr(plagiarism, "load_reference", fake_loader)

    sus = ["hello", "world", "icog"]
    result = plagiarism.scan_suspect(sus, k=k)

    assert result["total_ngrams"] == 2
    assert result["matched_count"] == 1
    assert result["score_percent"] == 50.0
