import pytest
from backend.semantic_hashing import (
    build_synonym_map,
    normalize_tokens,
    encode_tokens_syn,
    rolling_hash_syn
)

# Mock vocab for testing
VOCAB = {
    "car": 1,
    "vehicle": 2,
    "happy": 3,
    "sad": 4,
    "unhappy": 5
}

def test_synonym_mapping_basic():
    tokens = ["automobile", "car"]
    syn_map = build_synonym_map(tokens)

    # WordNet maps automobile → car
    assert syn_map["automobile"] == "car"
    assert syn_map["car"] == "car"

def test_normalization():
    tokens = ["automobile", "car"]
    syn_map = build_synonym_map(tokens)
    normalized = normalize_tokens(tokens, syn_map)

    assert normalized == ["car", "car"]

def test_encode_tokens_syn():
    tokens = ["automobile", "car"]
    syn_map = build_synonym_map(tokens)
    encoded = encode_tokens_syn(tokens, VOCAB, syn_map)

    # Both should encode to "car" → 1
    assert encoded == [1, 1]

def test_rolling_hash_syn():
    tokens = ["automobile", "car", "vehicle"]
    syn_map = build_synonym_map(tokens)

    hashes = rolling_hash_syn(tokens, VOCAB, k=2, synonym_map=syn_map)

    # IDs:
    # automobile→car  => 1
    # car             => 1
    # vehicle         => 2
    #
    # Hashes should be pairs: (hash_value, start_index)
    # Example structure:
    # [(X,0),(Y,1)]
    assert len(hashes) == len(tokens) - 2 + 1
    assert all(isinstance(h[1], int) for h in hashes)
    assert all(h[1] >= 0 for h in hashes)
