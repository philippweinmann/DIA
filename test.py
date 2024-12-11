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

    def _verbose_assert(self, search_function, doc_id, word, expected, dist=None):
        if dist is not None:
            assert (doc_id in search_function(word, dist)) == expected, f"Expected {doc_id} in result of search for {word} to be {expected}"
        else:
            assert (doc_id in search_function(word)) == expected, f"Expected {doc_id} in result of search for {word} to be {expected}"

    def _common_exact_search(self, search_func):
        # this should work for exact_search, hamming_search, and levshetin_search
        self._verbose_assert(search_func, self.doc_1_id, self.in_neither_string, False)
        self._verbose_assert(search_func, self.doc_2_id, self.in_neither_string, False)

        self._verbose_assert(search_func, self.doc_1_id, self.only_in_doc_1, True)
        self._verbose_assert(search_func, self.doc_2_id, self.only_in_doc_1, False)

        self._verbose_assert(search_func, self.doc_1_id, self.only_in_doc_2, False)
        self._verbose_assert(search_func, self.doc_2_id, self.only_in_doc_2, True)

        self._verbose_assert(search_func, self.doc_1_id, self.in_both_docs, True)
        self._verbose_assert(search_func, self.doc_2_id, self.in_both_docs, True)

    def test_exact_match(self):
        self._common_exact_search(self.trie.exact_search)

    def _common_hamming_search(self, search_func):
        # this should work for hamming_search, and levshetin_search
                # let's add some strings for hamming tests
        self.hamm_dist_1 = ["applr", "rpple", "apble"]
        self.hamm_dist_2 = ["apprr", "rprle", "rpble"]
        
        for word in self.hamm_dist_1:
            self._verbose_assert(search_func, self.doc_1_id, word, False, 0)
            self._verbose_assert(search_func, self.doc_1_id, word, True, 1)
            self._verbose_assert(search_func, self.doc_1_id, word, True, 2)

        for word in self.hamm_dist_2:
            self._verbose_assert(search_func, self.doc_1_id, word, False, 0)
            self._verbose_assert(search_func, self.doc_1_id, word, False, 1)
            self._verbose_assert(search_func, self.doc_1_id, word, True, 2)
            self._verbose_assert(search_func, self.doc_1_id, word, True, 3)

    def test_hamming_distance(self):
        search_func = self.trie.hamming_search

        self._common_exact_search(search_func)
        self._common_hamming_search(search_func)
    
        for word in self.levshtein_dist_1_too_long:
            self._verbose_assert(search_func, self.doc_1_id, word, False, 0)
            self._verbose_assert(search_func, self.doc_1_id, word, False, 1)
            self._verbose_assert(search_func, self.doc_1_id, word, False, 2)

        for word in self.levshtein_dist_1_too_short:
            self._verbose_assert(search_func, self.doc_1_id, word, False, 0)
            self._verbose_assert(search_func, self.doc_1_id, word, False, 1)
            self._verbose_assert(search_func, self.doc_1_id, word, False, 2)

    def test_levenshtein_distance(self):
        search_func = self.trie.levshetin_search
        
        self._common_exact_search(search_func)
        self._common_hamming_search(search_func)

        for word in self.levshtein_dist_1_too_long:
            self._verbose_assert(search_func, self.doc_1_id, word, False, 0)
            self._verbose_assert(search_func, self.doc_1_id, word, True, 1)
            self._verbose_assert(search_func, self.doc_1_id, word, True, 2)

        for word in self.levshtein_dist_1_too_short:
            self._verbose_assert(search_func, self.doc_1_id, word, False, 0)
            self._verbose_assert(search_func, self.doc_1_id, word, True, 1)
            self._verbose_assert(search_func, self.doc_1_id, word, True, 2)

        # now we test for words that will match multiple documents but in different nodes.
        self.trie.insert("ab", self.doc_1_id)
        self.trie.insert("ba", self.doc_2_id)

        self._verbose_assert(search_func, self.doc_1_id, "a", True, 1)
        self._verbose_assert(search_func, self.doc_2_id, "a", True, 1)

        self.trie.insert("c", self.doc_1_id)
        self.trie.insert("d", self.doc_2_id)

        self._verbose_assert(search_func, self.doc_1_id, "cd", True, 1)
        self._verbose_assert(search_func, self.doc_2_id, "cd", True, 1)
        self._verbose_assert(search_func, self.doc_1_id, "cde", False, 1)


if __name__ == '__main__':
    unittest.main()