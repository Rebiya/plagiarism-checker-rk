import pytest
import pickle
from backend import trie_builder

def test_trie_node_insert_and_build():
    root = trie_builder.TrieNode()
    root.insert("hello")
    root.insert("helium")

    assert "h" in root.children
    assert root.children["h"].children["e"].children["l"].children["l"].children["o"].is_end_of_word

def test_build_trie_and_save_load(tmp_path):
    tokens = ["hello", "helium", "hi"]
    trie = trie_builder.build_trie(tokens)

    assert isinstance(trie, trie_builder.TrieNode)

    # Save
    path = tmp_path / "trie.pkl"
    trie_builder.save_trie(trie, str(path))
    assert path.exists()

    # Load back manually
    with open(path, "rb") as f:
        loaded_trie = pickle.load(f)

    assert isinstance(loaded_trie, trie_builder.TrieNode)
    assert loaded_trie.children["h"].children["e"].children["l"].children["l"].children["o"].is_end_of_word

def test_load_tokenized_reference(tmp_path):
    file = tmp_path / "tokens.txt"
    file.write_text("a b c d")
    tokens = trie_builder.load_tokenized_reference(str(file))
    assert tokens == ["a", "b", "c", "d"]

    # test FileNotFoundError
    with pytest.raises(FileNotFoundError):
        trie_builder.load_tokenized_reference(str(tmp_path / "not_exist.txt"))
