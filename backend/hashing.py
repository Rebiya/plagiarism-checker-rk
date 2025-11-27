import os
import pickle
from typing import Dict, List, Tuple, Set

# Larger constants for fewer collisions
DEFAULT_B = 257
DEFAULT_M = 10**9 + 7


# ===================================
# 1. Create vocabulary mapping
# ===================================
def word_ids(tokens: List[str]) -> Dict[str, int]:
    """
    Build word -> integer mapping
    Deterministic based on first appearance order.
    """
    vocab = {}
    next_id = 1
    for t in tokens:
        if t not in vocab:
            vocab[t] = next_id
            next_id += 1
    return vocab


# ===================================
# 2. Convert tokens to int IDs
# ===================================
def encode_tokens(tokens: List[str], vocab: Dict[str, int]) -> List[int]:
    """
    Encode tokens — unknown tokens ignored.
    """
    return [vocab[t] for t in tokens if t in vocab]


# ===================================
# 3. Rolling Hash (Rabin–Karp)
# ===================================
def rolling_hash(ids: List[int], k: int,
                 B: int = DEFAULT_B,
                 M: int = DEFAULT_M) -> List[Tuple[int, int]]:
    """Compute rolling hashes for n-grams."""
    n = len(ids)
    if n < k:
        return []

    current = 0
    out: List[Tuple[int, int]] = []

    power = pow(B, k-1, M)  # B^(k-1)

    # initial window
    for i in range(k):
        current = (current * B + ids[i]) % M
    out.append((current, 0))

    # slide
    for i in range(k, n):
        current = (current - (ids[i-k] * power)) % M
        current = (current * B + ids[i]) % M
        out.append((current, i-k+1))

    return out


# ===================================
# 4. Save reference hashes/vocab
# ===================================
def save_reference(hash_set: Set[int], vocab: Dict[str, int],
                   hash_path: str, vocab_path: str):
    os.makedirs(os.path.dirname(hash_path), exist_ok=True)

    with open(hash_path, "wb") as f:
        pickle.dump(hash_set, f)
    with open(vocab_path, "wb") as f:
        pickle.dump(vocab, f)

    print(f"[OK] saved hash set → {hash_path}")
    print(f"[OK] saved vocab → {vocab_path}")


# ===================================
# 5. Load reference
# ===================================
def load_reference(hash_path: str, vocab_path: str) -> Tuple[Set[int], Dict[str, int]]:
    with open(hash_path, "rb") as f:
        h = pickle.load(f)
    with open(vocab_path, "rb") as f:
        v = pickle.load(f)
    return h, v
