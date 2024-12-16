import unittest
from pygtrie import CharTrie
from trie_utils import input_query_in_trie

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = CharTrie()

    def test_insert_int_trie(self):
        query_words = ['hello', 'world']
        query_id, query_type, query_dist, query_words = 1, 0, 0, query_words
        input_query_in_trie(self.trie, query_id, query_type, query_dist, query_words)
        assert len(self.trie) == len(query_words)

        hamming_distance = 0
        self.trie.clear()
        query_id, query_type, query_dist, query_words = 1, 1, hamming_distance, query_words
        input_query_in_trie(self.trie, query_id, query_type, query_dist, query_words)
        assert len(self.trie) == len(query_words)

        hamming_distance = 1
        self.trie.clear()
        query_id, query_type, query_dist, query_words = 1, 1, hamming_distance, query_words
        input_query_in_trie(self.trie, query_id, query_type, query_dist, query_words)

        input_length = len(query_words)
        for word in query_words:
            input_length += len(word)
        
        print(input_length)
        print(len(self.trie))
        print(self.trie)
        assert len(self.trie) == input_length
        

if __name__ == '__main__':
    unittest.main()