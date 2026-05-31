class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.words = []

    def put(self, word, value=None):
        if not isinstance(word, str):
            raise TypeError("word must be string")

        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]

        node.is_end = True
        self.words.append(word)


class Homework(Trie):

    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be string")

        if pattern == "":
            return 0

        return sum(1 for w in self.words if w.endswith(pattern))

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError("prefix must be string")

        if prefix == "":
            return False

        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]

        return True


if __name__ == "__main__":
    trie = Homework()

    words = ["apple", "application", "banana", "cat"]
    for i, w in enumerate(words):
        trie.put(w, i)

    assert trie.count_words_with_suffix("e") == 1
    assert trie.count_words_with_suffix("ion") == 1
    assert trie.count_words_with_suffix("a") == 1
    assert trie.count_words_with_suffix("at") == 1
    assert trie.count_words_with_suffix("") == 0

    assert trie.has_prefix("app") is True
    assert trie.has_prefix("bat") is False
    assert trie.has_prefix("ban") is True
    assert trie.has_prefix("ca") is True
    assert trie.has_prefix("") is False

    print("ALL TESTS PASSED ✔")