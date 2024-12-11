import unittest
from trie import Trie

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        self.doc_1_id = 1
        self.doc_2_id = 2

        self.in_neither_string = "NOTINTEITHERDOCS"
        self.only_in_doc_1 = "apple"
        self.only_in_doc_2 = "peach"
        self.in_both_docs = "banana"

        self.trie.insert(self.only_in_doc_1, self.doc_1_id)
        self.trie.insert(self.only_in_doc_2, self.doc_2_id)

        self.trie.insert(self.in_both_docs, self.doc_1_id)
        self.trie.insert(self.in_both_docs, self.doc_2_id)

        self.levshtein_dist_1_too_long = ["appler", "rapple", "apbple"]
        self.levshtein_dist_1_too_short = ["pple", "appl", "aple"]

    def _common_exact_search(self, search_func):
        # this should work for exact_search, hamming_search, and levshetin_search
        assert self.doc_1_id not in search_func(self.in_neither_string)
        assert self.doc_2_id not in search_func(self.in_neither_string)

        assert self.doc_1_id in search_func(self.only_in_doc_1)
        assert self.doc_2_id not in search_func(self.only_in_doc_1)

        assert self.doc_1_id not in search_func(self.only_in_doc_2)
        assert self.doc_2_id in search_func(self.only_in_doc_2)

        assert self.doc_1_id in search_func(self.in_both_docs)
        assert self.doc_2_id in search_func(self.in_both_docs)

    def test_exact_match(self):
        self._common_exact_search(self.trie.exact_search)

    def _common_hamming_search(self, search_func):
        # this should work for hamming_search, and levshetin_search
                # let's add some strings for hamming tests
        self.hamm_dist_1 = ["applr", "rpple", "apble"]
        self.hamm_dist_2 = ["apprr", "rprle", "rpble"]
        
        for word in self.hamm_dist_1:
            assert self.doc_1_id not in search_func(word, 0)
            assert self.doc_1_id in search_func(word, 1)
            assert self.doc_1_id in search_func(word, 2)

        for word in self.hamm_dist_2:
            assert self.doc_1_id not in search_func(word, 0)
            assert self.doc_1_id not in search_func(word, 1)
            assert self.doc_1_id in search_func(word, 2)
            assert self.doc_1_id in search_func(word, 3)

        for word in self.levshtein_dist_1_too_long:
            assert self.doc_1_id not in search_func(word, 0)
            assert self.doc_1_id not in search_func(word, 1)
            assert self.doc_1_id not in search_func(word, 2)

        for word in self.levshtein_dist_1_too_short:
            assert self.doc_1_id not in search_func(word, 0)
            assert self.doc_1_id not in search_func(word, 1)
            assert self.doc_1_id not in search_func(word, 2)

    def test_hamming_distance(self):
        self._common_exact_search(self.trie.hamming_search)
        self._common_hamming_search(self.trie.hamming_search)

    def test_levenshtein_distance(self):
        self._common_exact_search(self.trie.levenshtein_search)
        self._common_hamming_search(self.trie.levshetin_search)

        for word in self.levshtein_dist_1_too_long:
            assert self.doc_1_id not in self.trie.levshetin_search(word, 0)
            assert self.doc_1_id in self.trie.levshetin_search(word, 1)
            assert self.doc_1_id in self.trie.levshetin_search(word, 2)

        for word in self.levshtein_dist_1_too_short:
            assert self.doc_1_id not in self.trie.levshetin_search(word, 0)
            assert self.doc_1_id in self.trie.levshetin_search(word, 1)
            assert self.doc_1_id in self.trie.levshetin_search(word, 2)

        # now we test for words that will match multiple documents but in different nodes.
        self.trie.insert("ab", self.doc_1_id)
        self.trie.insert("ba", self.doc_2_id)

        assert self.doc_1_id in self.trie.levshetin_search("a", 1)
        assert self.doc_2_id in self.trie.levshetin_search("a", 1)

        self.trie.insert("c", self.doc_1_id)
        self.trie.insert("d", self.doc_2_id)

        assert self.doc_1_id in self.trie.levshetin_search("cd", 1)
        assert self.doc_2_id in self.trie.levshetin_search("cd", 1)


if __name__ == '__main__':
    unittest.main()