"""
Pipeline layer to unify cleaning → tokenizing → hashing → plagiarism scan.
Used by Streamlit or FastAPI.
"""

from typing import Dict, Any, List

from backend.text_processing import clean_text
from backend.tokenizer import tokenize_text
from backend.plagiarism import (
    load_reference,
    compute_suspect_hashes,
    compare_hashes,
    compute_plagiarism_score,
    DEFAULT_K,
    DEFAULT_B,
    DEFAULT_M
)
from backend.semantic_hashing import build_synonym_map, rolling_hash_syn, encode_tokens_syn, normalize_tokens

def plagiarism_pipeline(raw_text: str,
                        k: int = DEFAULT_K,
                        B: int = DEFAULT_B,
                        M: int = DEFAULT_M,
                        use_synonyms: bool = False) -> Dict[str, Any]:



    """
    Full pipeline for suspect scan with optional synonym-awareness:
      1. Clean text
      2. Tokenize
      3. Load saved reference (hash set + vocab)
      4. Compute suspect hashes
      5. Compare
      6. Return structured score + metadata
    """

    # Step 1 -> Clean
    cleaned = clean_text(raw_text)

    # Step 2 -> Tokens
    tokens: List[str] = tokenize_text(cleaned)

    # Step 3 -> Load reference from disk
    reference_hashes, vocab = load_reference()

    # Step 4 -> Compute hashes against reference vocab

    if use_synonyms:
        # Synonym-aware hashes
        syn_map = build_synonym_map(tokens)
        suspect_pairs = rolling_hash_syn(tokens, vocab, k=k, synonym_map=syn_map)
    else:
        # Original hashing
        suspect_pairs = compute_suspect_hashes(tokens, vocab, k=k, B=B, M=M)

    matched, total, matched_pairs = compare_hashes(suspect_pairs, reference_hashes)
    score = compute_plagiarism_score(matched, total)

    return {
        "cleaned_text": cleaned[:300],     # small debug preview
        "tokens": len(tokens),
        "ngrams_total": total,
        "ngrams_matched": matched,
        "score_percent": score,
        "matches": matched_pairs,
        "k": k,
        "use_synonyms": use_synonyms
    }
