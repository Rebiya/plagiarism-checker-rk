#!/usr/bin/env python3
# use " python -m backend.ref_builder " to run this script
"""
run_build_reference.py

Simple runner script that:
 - tokenizes a cleaned reference file
 - builds reference vocab + n-gram hashes
 - saves reference_hashes.pkl and vocab.pkl to disk

Usage (from project root):
    python backend/Reference_runners/run_build_reference.py
Or (module mode):
    python -m backend.Reference_runners.run_build_reference

You may pass optional args:
    python backend/Reference_runners/run_build_reference.py --input data/cleaned_data/all_cleaned.txt --k 10

This script is defensive about import paths so you can run it from project root.
"""

import argparse
import os
import sys

# --- Make imports work even if run directly ---
# If this script sits in backend/Reference_runners, project_root is two levels up.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now import your modules
from backend import tokenizer
from backend import plagiarism

def main():
    p = argparse.ArgumentParser(description="Build reference hash set from cleaned text.")
    p.add_argument(
        "--input",
        "-i",
        default=os.path.join("data", "cleaned_data", "all_cleaned.txt"),
        help="Path to cleaned reference text file (tokenizable)."
    )
    p.add_argument(
        "--k",
        "-k",
        type=int,
        default=10,
        help="n-gram window size for rolling hash (default: 10). Use larger values for longer matches."
    )
    p.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print verbose logs"
    )
    args = p.parse_args()

    input_path = args.input
    k = args.k
    verbose = args.verbose

    if not os.path.exists(input_path):
        print(f"[ERROR] Input file not found: {input_path}")
        sys.exit(1)

    # 1) Tokenize reference file
    tokens = tokenizer.tokenize_file(input_path)
    if verbose:
        print(f"[INFO] Tokenized reference file: {input_path}")
        print(f"[INFO] Tokens count: {len(tokens)}")

    # 2) Build reference (vocab + hash set) and save to disk
    # uses plagiarism.build_reference_from_tokens which wraps hashing functions and saves
    hash_set, vocab = plagiarism.build_reference_from_tokens(tokens, k=k)

    # 3) Print summary
    # The plagiarism module prints "Saved reference ..." already; show counts too.
    print("=== Reference build summary ===")
    print(f"Input file        : {input_path}")
    print(f"Tokens             : {len(tokens)}")
    print(f"Vocab size         : {len(vocab)}")
    print(f"Unique hashes      : {len(hash_set)}")
    print(f"n-gram window k    : {k}")
    print("==============================")

if __name__ == "__main__":
    main()
