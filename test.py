import unittest
from trie import Trie

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        strings = ["apple", "app", "ap", "applesauce", "banana", "bananas", "bananarama", "bananaramas"]

        for string in strings:
            self.trie.insert(string)
        return super().setUp()

    def test_exact_match(self):
        assert self.trie.exact_search("apple") == True
        assert self.trie.exact_search("app") == True
        assert self.trie.exact_search("NotExistent") == False

    def test_hamming_distance(self):
        assert self.trie.hamming_search("apple", 0) == True
        assert self.trie.hamming_search("apple", 1) == True

        assert self.trie.hamming_search("applr", 0) == False
        assert self.trie.hamming_search("applr", 1) == True
        assert self.trie.hamming_search("applr", 2) == True

    def test_levenshtein_distance(self):
        assert self.trie.levshetin_search("apple", 0) == True
        assert self.trie.levshetin_search("apple", 1) == True
        assert self.trie.levshetin_search("applr", 0) == False
        assert self.trie.levshetin_search("applr", 1) == True
        assert self.trie.levshetin_search("applr", 2) == True

        assert self.trie.levshetin_search("appl", 1) == True

        assert self.trie.levshetin_search("appl", 0) == False
        assert self.trie.levshetin_search("rppl", 2) == True
        assert self.trie.levshetin_search("rppl", 3) == True

if __name__ == '__main__':
    unittest.main()
