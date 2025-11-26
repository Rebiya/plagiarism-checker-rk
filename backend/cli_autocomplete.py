# to run use" python -m backend.cli_autocomplete" 
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from backend.trie_runtime import load_trie, suggest_words
import os

TRIE_FILE = os.path.join("data", "trie", "trie.pkl")
trie = load_trie(TRIE_FILE)

class TrieCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        parts = text.split()
        if not parts:
            return

        prefix = parts[-1]
        suggestions = suggest_words(prefix, trie, max_results=10)
        for s in suggestions:
            yield Completion(
                s,
                start_position=-len(prefix),  # replace only last token
                display=s
            )

session = PromptSession(completer=TrieCompleter())

print("\n🚀 Google-style Trie autocomplete CLI. Type and see suggestions.\n")

while True:
    try:
        user_input = session.prompt("> ")
        print("You entered:", user_input)
    except KeyboardInterrupt:
        continue
    except EOFError:
        break

print("bye 👋")
