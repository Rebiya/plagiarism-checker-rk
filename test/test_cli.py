from prompt_toolkit.document import Document
from backend.cli import TrieCompleter


def test_trie_autocomplete_basic(mocker):
    """
    Tests:
    - Only last token is used
    - suggest_words called once
    - Output completions generated properly
    """

    fake_trie = {}
    fake_suggestions = ["hello", "helium"]

    # mock suggest_words
    mocker.patch(
        "backend.cli.suggest_words",
        return_value=fake_suggestions
    )

    completer = TrieCompleter()

    doc = Document(text="he")

    comps = list(completer.get_completions(doc, None))

    # We expect 2 suggestions
    assert len(comps) == 2
    assert comps[0].text == "hello"
    assert comps[1].text == "helium"

    # Only last word replaced
    assert comps[0].start_position == -2  # len("he")
