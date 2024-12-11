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

    def test_exact_match(self):
        assert self.doc_1_id not in self.trie.exact_search(self.in_neither_string)
        assert self.doc_2_id not in self.trie.exact_search(self.in_neither_string)

        assert self.doc_1_id in self.trie.exact_search(self.only_in_doc_1)
        assert self.doc_2_id not in self.trie.exact_search(self.only_in_doc_1)

        assert self.doc_1_id not in self.trie.exact_search(self.only_in_doc_2)
        assert self.doc_2_id in self.trie.exact_search(self.only_in_doc_2)

        assert self.doc_1_id in self.trie.exact_search(self.in_both_docs)
        assert self.doc_2_id in self.trie.exact_search(self.in_both_docs)

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
