"""
CLI with Google-style Trie Autocomplete + Plagiarism Scan

USAGE:
    python -m backend.cli_autocomplete
"""

import os
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion

from backend.trie_runtime import load_trie, suggest_words
from backend.pipeline import plagiarism_pipeline

# ============================================
# Load Trie
# ============================================
TRIE_FILE = os.path.join("data", "trie", "trie.pkl")
trie = load_trie(TRIE_FILE)


# ============================================
# Autocomplete Component
# ============================================
class TrieCompleter(Completer):
    """
    Autocomplete replaces ONLY the last token, like Google.
    """

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()

        if not text:
            return

        words = text.split()
        prefix = words[-1]

        # fetch from trie
        suggestions = suggest_words(prefix, trie, max_results=10)

        for s in suggestions:
            yield Completion(
                s,
                start_position=-len(prefix),   # replace only last word
                display=s
            )


session = PromptSession(completer=TrieCompleter())


# ============================================
# CLI APPLICATION
# ============================================
print("\n🔥 Trie Autocomplete + Plagiarism Checker CLI")
print("Type your text. Suggestions show live.")
print("Press ENTER to run plagiarism scan.")
print("Type 'exit' to quit.\n")

while True:
    try:
        user_input = session.prompt("> ").strip()

        # -------- exit condition --------
        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        print("\n🔍 Running plagiarism detection...\n")

        result = plagiarism_pipeline(user_input, use_synonyms=True)

        print(f"🧠 Tokens: {result['tokens']}")
        print(f"📊 Total n-grams: {result['ngrams_total']}")
        print(f"⚠️ Matched n-grams: {result['ngrams_matched']}")
        print(f"🏷️ Score: {result['score_percent']:.2f}% (similarity)")

        # Optional details
        if result["matches"]:
            print("\n🔗 Matched n-grams (first 10):")
            for m in result["matches"][:10]:
                print(f"  - Hash {m[0]} at index {m[1]}")
        else:
            print("\n✨ No matches found.")

        print("\n────────────────────────────────────\n")

    except KeyboardInterrupt:
        # Ctrl+C keeps the CLI running
        continue
    except EOFError:
        # Ctrl+D exits
        break

print("\n👋 Bye!\n")
