import pytest
from backend import trie_runtime
from backend.trie_builder import TrieNode
import pickle

def test_suggest_words_basic():
    root = TrieNode()
    for w in ["hello", "helium", "hi", "habit"]:
        root.insert(w)

    # prefix 'he'
    results = trie_runtime.suggest_words("he", root)
    assert "hello" in results
    assert "helium" in results
    assert all(r.startswith("he") for r in results)

    # prefix not in trie
    assert trie_runtime.suggest_words("xyz", root) == []

def test_load_trie_and_fixed_unpickler(tmp_path):
    # build a trie
    root = TrieNode()
    root.insert("hello")

    path = tmp_path / "trie.pkl"
    with open(path, "wb") as f:
        pickle.dump(root, f)

    loaded = trie_runtime.load_trie(str(path))
    assert isinstance(loaded, TrieNode)
    assert "h" in loaded.children
