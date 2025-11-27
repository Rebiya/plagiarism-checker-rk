import pytest
from backend.pipeline import plagiarism_pipeline

# We will monkeypatch these imports
from backend import pipeline


def test_plagiarism_pipeline_full(mocker):
    """
    Tests full pipeline logic:
    clean → tokenize → load_reference → hashing → compare → score
    without using real files.
    """

    # ---------------------
    # Step 1: clean
    # ---------------------
    mocker.patch.object(
        pipeline, "clean_text",
        return_value="hello world hello"
    )

    # ---------------------
    # Step 2: tokenize
    # ---------------------
    mocker.patch.object(
        pipeline, "tokenize_text",
        return_value=["hello", "world", "hello"]
    )

    # ---------------------
    # Step 3: reference loader
    # ---------------------
    fake_ref_hashes = {1111, 2222}
    fake_vocab = {"hello": 1, "world": 2}

    mocker.patch.object(
        pipeline, "load_reference",
        return_value=(fake_ref_hashes, fake_vocab)
    )

    # ---------------------
    # Step 4: hashing
    # ---------------------
    fake_pairs = [(1111, 0), (3333, 1)]  # 1 match, 1 miss

    mocker.patch.object(
        pipeline, "compute_suspect_hashes",
        return_value=fake_pairs
    )

    # ---------------------
    # Step 5: compare
    # ---------------------
    mocker.patch.object(
        pipeline, "compare_hashes",
        return_value=(1, 2, [(1111, 0)])
    )

    # ---------------------
    # Step 6: score
    # ---------------------
    mocker.patch.object(
        pipeline, "compute_plagiarism_score",
        return_value=50.0
    )

    result = plagiarism_pipeline("RAW TEXT")

    # ---------------------
    # Assertions
    # ---------------------
    assert result["cleaned_text"] == "hello world hello"
    assert result["tokens"] == 3
    assert result["ngrams_total"] == 2
    assert result["ngrams_matched"] == 1
    assert result["score_percent"] == 50.0
    assert result["matches"] == [(1111, 0)]
    assert result["k"] > 0
