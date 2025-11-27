import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict

# Ensure WordNet data is downloaded
try:
    wn.synsets("test")
except LookupError:
    nltk.download("wordnet")
    nltk.download("omw-1.4")

# -------------------------------
# Build synonym mapping
# -------------------------------
def build_synonym_map(tokens: List[str]) -> Dict[str, str]:
    """
    Map each token to a canonical synonym.
    - For each word, choose the first lemma of its first synset as canonical form.
    - If no synset found, keep the original word.
    """
    mapping = {}
    for t in tokens:
        synsets = wn.synsets(t)
        if synsets:
            # pick first lemma of first synset
            lemma = synsets[0].lemmas()[0].name().lower()
            mapping[t] = lemma
        else:
            mapping[t] = t
    return mapping

# -------------------------------
# Normalize tokens using synonyms
# -------------------------------
def normalize_tokens(tokens: List[str], synonym_map: Dict[str, str]) -> List[str]:
    """
    Replace each token with its canonical synonym form.
    """
    return [synonym_map.get(t, t) for t in tokens]

# -------------------------------
# Encode tokens with optional synonym normalization
# -------------------------------
def encode_tokens_syn(tokens: List[str], vocab: Dict[str, int], synonym_map: Dict[str, str]) -> List[int]:
    """
    Map tokens → canonical synonym form → encode with vocab
    """
    normalized = normalize_tokens(tokens, synonym_map)
    return [vocab[t] for t in normalized if t in vocab]

# -------------------------------
# Example integration with rolling hash
# -------------------------------
from backend.hashing import rolling_hash

def rolling_hash_syn(tokens: List[str], vocab: Dict[str, int], k: int, synonym_map: Dict[str, str]):
    """
    Compute Rabin-Karp hashes over synonym-normalized tokens
    """
    ids = encode_tokens_syn(tokens, vocab, synonym_map)
    return rolling_hash(ids, k)

