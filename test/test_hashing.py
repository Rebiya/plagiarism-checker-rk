"""
Plagiarism checker logic using Rabin–Karp hashing.

Responsibilities:
- Build reference hash set + vocabulary and save to disk
- Load saved reference + vocab
- Compute suspect rolling-hash list (in-memory)
- Compare suspect hashes against reference set
- Return similarity score + matched metadata
"""

import os
import pickle
from typing import Dict, List, Set, Tuple, Any

# from . import hashing   # <--- RELATIVE import, works when executed as package
from backend import hashing


# Default storage paths
HASHED_DIR = os.path.join("data", "hashed")
REF_HASHES_PATH = os.path.join(HASHED_DIR, "reference_hashes.pkl")
VOCAB_PATH = os.path.join(HASHED_DIR, "vocab.pkl")

# Default RK parameters
DEFAULT_K = 10
DEFAULT_B = hashing.DEFAULT_B
DEFAULT_M = hashing.DEFAULT_M


# ====================================================
# UTILS: Save / Load
# ====================================================

def _ensure_hashed_dir():
    os.makedirs(HASHED_DIR, exist_ok=True)


def save_reference(hash_set: Set[int],
                   vocab: Dict[str, int],
                   hashes_path: str = REF_HASHES_PATH,
                   vocab_path: str = VOCAB_PATH):
    """Store reference hash set + vocab to disk."""
    _ensure_hashed_dir()

    with open(hashes_path, "wb") as f:
        pickle.dump(hash_set, f)

    with open(vocab_path, "wb") as f:
        pickle.dump(vocab, f)

    print(f"[OK] Saved reference hashes → {hashes_path}")
    print(f"[OK] Saved vocab → {vocab_path}")


def load_reference(hashes_path: str = REF_HASHES_PATH,
                   vocab_path: str = VOCAB_PATH) -> Tuple[Set[int], Dict[str, int]]:
    """Load reference hashes + vocab."""
    if not os.path.exists(hashes_path):
        raise FileNotFoundError(f"Missing hash file: {hashes_path}")
    if not os.path.exists(vocab_path):
        raise FileNotFoundError(f"Missing vocab file: {vocab_path}")

    with open(hashes_path, "rb") as f:
        hash_set = pickle.load(f)
    with open(vocab_path, "rb") as f:
        vocab = pickle.load(f)

    return hash_set, vocab


# ====================================================
# BUILD REFERENCE
# ====================================================

def build_reference_from_tokens(tokens: List[str],
                                k: int = DEFAULT_K,
                                B: int = DEFAULT_B,
                                M: int = DEFAULT_M,
                                out_hash_path: str = REF_HASHES_PATH,
                                out_vocab_path: str = VOCAB_PATH):
    """
    Offline reference building step.

    Steps:
      1. Build vocabulary (word → int)
      2. Convert tokens->ids
      3. Compute rolling n-gram hashes (size k)
      4. Convert to a unique hash set
      5. Save vocab + hash set
    """
    vocab = hashing.word_ids(tokens)
    ids = hashing.encode_tokens(tokens, vocab)
    pairs = hashing.rolling_hash(ids, k=k, B=B, M=M)

    hash_set = {h for (h, _) in pairs}
    save_reference(hash_set, vocab, out_hash_path, out_vocab_path)

    return hash_set, vocab


def build_reference_from_cleaned_file(cleaned_file_path: str,
                                      k: int = DEFAULT_K,
                                      B: int = DEFAULT_B,
                                      M: int = DEFAULT_M):
    """
    Utility: Build reference from a pre-tokenized text file.
    NOTE: assumes tokens separated by whitespace already.
    """
    if not os.path.exists(cleaned_file_path):
        raise FileNotFoundError(cleaned_file_path)

    with open(cleaned_file_path, "r", encoding="utf-8") as f:
        tokens = f.read().strip().split()

    return build_reference_from_tokens(tokens, k=k, B=B, M=M)


# ====================================================
# SUSPECT HASHES
# ====================================================

def compute_suspect_hashes(tokens: List[str],
                           vocab: Dict[str, int],
                           k: int = DEFAULT_K,
                           B: int = DEFAULT_B,
                           M: int = DEFAULT_M):
    """
    Convert suspect tokens to IDs using ONLY reference vocab.
    Unknown words are ignored to maintain hash compatibility.
    """
    ids = [vocab[t] for t in tokens if t in vocab]
    return hashing.rolling_hash(ids, k=k, B=B, M=M)


# ====================================================
# COMPARISON
# ====================================================

def compare_hashes(sus_hashes: List[Tuple[int, int]],
                   reference_hash_set: Set[int]):
    """
    Return:
     matched_count
     total_ngrams
     matched_pairs
    """
    total = len(sus_hashes)
    matched_pairs = [x for x in sus_hashes if x[0] in reference_hash_set]
    return len(matched_pairs), total, matched_pairs


def compute_plagiarism_score(matched_count: int,
                             total_sus_ngrams: int) -> float:
    """% of suspect n-grams found in reference."""
    if total_sus_ngrams == 0:
        return 0.0
    return 100 * (matched_count / total_sus_ngrams)


# ====================================================
# MAIN API: SCAN
# ====================================================

def scan_suspect(tokens: List[str],
                 k: int = DEFAULT_K,
                 B: int = DEFAULT_B,
                 M: int = DEFAULT_M):
    """
    End-to-end suspect scan:
      - loads saved reference
      - computes suspect hashes
      - compares
      - returns score + metadata
    """
    ref_hashes, vocab = load_reference()

    sus_pairs = compute_suspect_hashes(tokens, vocab, k=k, B=B, M=M)
    matched, total, matched_pairs = compare_hashes(sus_pairs, ref_hashes)

    return {
        "matched_count": matched,
        "total_ngrams": total,
        "score_percent": compute_plagiarism_score(matched, total),
        "matches": matched_pairs,
        "k": k
    }


# ====================================================
# CLI TESTING ENTRY POINT
# ====================================================

if __name__ == "__main__":
    print("This module shouldn't be run directly.")
    print("Use it from your app or scripts.\n")
