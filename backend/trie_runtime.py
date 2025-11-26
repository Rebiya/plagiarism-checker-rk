# backend/trie_runtime.py

import os
import pickle
from typing import List
from backend.trie_builder import TrieNode

# -----------------------------
# Fix pickle for Streamlit runtime
# -----------------------------
class FixedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == "TrieNode":
            from backend.trie_builder import TrieNode
            return TrieNode
        return super().find_class(module, name)

# -----------------------------
# Load Trie from Disk
# -----------------------------
def load_trie(path: str) -> TrieNode:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Trie file not found: {path}")
    with open(path, "rb") as f:
        trie_root: TrieNode = FixedUnpickler(f).load()
    print(f"[OK] Trie loaded from {path}")
    return trie_root

# -----------------------------
# Suggest Words for Autocomplete
# -----------------------------
def suggest_words(prefix: str, trie: TrieNode, max_results: int = 5) -> List[str]:
    results: List[str] = []

    def dfs(node: TrieNode, path: str):
        if len(results) >= max_results:
            return
        if node.is_end_of_word:
            results.append(path)
        for char, child in sorted(node.children.items()):
            dfs(child, path + char)

    # Traverse the Trie along the prefix
    node = trie
    for char in prefix:
        if char in node.children:
            node = node.children[char]
        else:
            return results  # prefix not found

    # DFS to collect suggestions
    dfs(node, prefix)
    return results

# -----------------------------
# CLI Testing Example
# -----------------------------
if __name__ == "__main__":
    TRIE_FILE = os.path.join("data", "trie", "trie.pkl")
    trie = load_trie(TRIE_FILE)

    while True:
        prefix = input("Enter prefix (or 'exit'): ").strip()
        if prefix.lower() == "exit":
            break
        suggestions = suggest_words(prefix, trie)
        print("Suggestions:", suggestions)
