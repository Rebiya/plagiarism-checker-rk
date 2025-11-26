# backend/trie_builder.py

import os
import pickle
from typing import Dict, List, Optional

# -----------------------------
# Trie Node Definition
# -----------------------------
class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end_of_word: bool = False

    def insert(self, word: str):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

# -----------------------------
# Build Trie from Tokens
# -----------------------------
def build_trie(tokens: List[str]) -> TrieNode:
    root = TrieNode()
    for token in tokens:
        root.insert(token)
    print(f"[OK] Trie built with {len(tokens)} tokens")
    return root

# -----------------------------
# Save Trie to Disk
# -----------------------------
def save_trie(trie: TrieNode, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(trie, f)
    print(f"[OK] Trie saved to {path}")

# -----------------------------
# Load Tokenized Reference from File
# -----------------------------
def load_tokenized_reference(file_path: str) -> List[str]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Reference file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    tokens = text.split()
    print(f"[OK] Loaded {len(tokens)} tokens from reference file")
    return tokens

# -----------------------------
# CLI / Offline Build Helper
# -----------------------------
if __name__ == "__main__":
    REF_FILE = os.path.join("data", "cleaned_data", "all_cleaned.txt")
    TRIE_FILE = os.path.join("data", "trie", "trie.pkl")

    tokens = load_tokenized_reference(REF_FILE)
    trie_root = build_trie(tokens)
    save_trie(trie_root, TRIE_FILE)
