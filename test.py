import unittest
from pygtrie import CharTrie
from trie_utils import input_query_in_trie, get_deletions_for_document, find_document_matches
from math import comb

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = CharTrie()

    def _iterate_trie(self, trie):
        # count the number of leafnodes in the trie:
        counter = 0
        for key, value in trie.items():
            if value:
                counter += len(value)
            
        return counter

    def test_insert_int_trie(self):
        query_words = ['hello']
        query_id, query_type, query_dist, query_words = 1, 0, 0, query_words
        input_query_in_trie(self.trie, query_id, query_type, query_dist, query_words)
        assert self._iterate_trie(self.trie) == len(query_words)

        hamming_distance = 0
        self.trie.clear()
        query_id, query_type, query_dist, query_words = 1, 1, hamming_distance, query_words
        input_query_in_trie(self.trie, query_id, query_type, query_dist, query_words)
        assert self._iterate_trie(self.trie) == len(query_words)

        hamming_distance = 1
        self.trie.clear()
        query_id, query_type, query_dist, query_words = 1, 1, hamming_distance, query_words
        input_query_in_trie(self.trie, query_id, query_type, query_dist, query_words)

        input_length = len(query_words)
        for word in query_words:
            input_length += len(word)

        assert self._iterate_trie(self.trie) == input_length

        hamming_distance = 2
        self.trie.clear()
        query_id, query_type, query_dist, query_words = 1, 1, hamming_distance, query_words
        input_query_in_trie(self.trie, query_id, query_type, query_dist, query_words)

        # calculate the amount of deletions up to hamming distance 2
        input_length = len(query_words)
        for word in query_words:
            input_length += len(word)
            input_length += len(word) * (len(word) - 1) // 2

        assert self._iterate_trie(self.trie) == input_length

        # levenshtein (works the same way as hamming distance for inserts)
        self.trie.clear()
        leven_distance = 0
        query_id, query_type, query_dist, query_words = 1, 2, leven_distance, query_words
        input_query_in_trie(self.trie, query_id, query_type, query_dist, query_words)
        assert self._iterate_trie(self.trie) == len(query_words)

        leven_distance = 1
        self.trie.clear()
        query_id, query_type, query_dist, query_words = 1, 2, leven_distance, query_words
        input_query_in_trie(self.trie, query_id, query_type, query_dist, query_words)

        input_length = len(query_words)
        for word in query_words:
            input_length += len(word)
        
        assert self._iterate_trie(self.trie) == input_length

        leven_distance = 2
        self.trie.clear()
        query_id, query_type, query_dist, query_words = 1, 2, leven_distance, query_words
        input_query_in_trie(self.trie, query_id, query_type, query_dist, query_words)

        # calculate the amount of deletions up to leven distance 2
        input_length = len(query_words)
        for word in query_words:
            input_length += len(word)
            input_length += len(word) * (len(word) - 1) // 2

        assert self._iterate_trie(self.trie) == input_length
        self.trie.clear()


    def _count_combinations(self, n, k_max):
        """
        Calculate the total number of combinations when replacing up to k_max items
        out of n items with a different type.

        Parameters:
        n (int): Total number of items.
        k_max (int): Maximum number of items to replace.

        Returns:
        int: Total number of combinations.
        """
        total_combinations = 0

        for k in range(0, k_max + 1):  # Iterate from 0 to k_max inclusively
            total_combinations += comb(n, k)

        return total_combinations


    def test_generate_document_masks(self):
        doc_id, doc_word_length, doc_contents = 1, 2, ['hello', 'world']

        for word in doc_contents:
            word_mask_tuples = get_deletions_for_document([word], max_dist=3)
            expected_combinations = self._count_combinations(len(word), 3)

            assert expected_combinations == len(word_mask_tuples)

    def _combined_exact_search(self, query_type):
        query_distance = 0

        self.trie.clear()

        # query_1:
        query_words_1 = ['hello', "world"]
        query_id_1, query_type_1, query_dist_1, query_words_1 = 1, query_type, query_distance, query_words_1
        input_query_in_trie(self.trie, query_id_1, query_type_1, query_dist_1, query_words_1)

        # query_2:
        query_words_2 = ['hello', "couchie"]
        query_id_2, query_type_2, query_dist_2, query_words_2 = 2, query_type, query_distance, query_words_2
        input_query_in_trie(self.trie, query_id_2, query_type_2, query_dist_2, query_words_2)

        # doc_1:
        doc_id, doc_word_length, doc_contents = 1, 1, ['hello']

        matches = find_document_matches(self.trie, doc_contents)
        assert matches == {query_id_1, query_id_2}

        # doc_2:
        doc_id, doc_word_length, doc_contents = 2, 1, ['hell']

        matches = find_document_matches(self.trie, doc_contents)
        assert matches == set()

        # multiple docs
        doc_id, doc_word_length, doc_contents = 4, 1, ['hello']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_1, query_id_2}

    def test_match_document_exact(self):
        self._combined_exact_search(0)

        self.trie.clear()
        query_type = 0
        query_distance = 0
        
        # query_1:
        query_words_1 = ['hello', "world"]
        query_id_1, query_type_1, query_dist_1, query_words_1 = 1, query_type, query_distance, query_words_1
        input_query_in_trie(self.trie, query_id_1, query_type_1, query_dist_1, query_words_1)

        # query_2:
        query_words_2 = ['hello', "couchie"]
        query_id_2, query_type_2, query_dist_2, query_words_2 = 2, query_type, query_distance, query_words_2
        input_query_in_trie(self.trie, query_id_2, query_type_2, query_dist_2, query_words_2)
        
        # doc_1:
        doc_id, doc_word_length, doc_contents = 1, 1, ['hellox']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == set()

    def test_match_hamming(self):
        self._combined_exact_search(1)

        self.trie.clear()

        hamming_distance = 1
        # let's try some basic hamming distance tests
        # query_1:
        query_words_1 = ['hello', "world"]
        query_id_1, query_type_1, query_dist_1, query_words_1 = 1, 1, hamming_distance, query_words_1
        input_query_in_trie(self.trie, query_id_1, query_type_1, query_dist_1, query_words_1)

        # query_2:
        query_words_2 = ['hello', "couchie"]
        query_id_2, query_type_2, query_dist_2, query_words_2 = 2, 1, hamming_distance, query_words_2
        input_query_in_trie(self.trie, query_id_2, query_type_2, query_dist_2, query_words_2)

        # doc_1:
        doc_id, doc_word_length, doc_contents = 1, 1, ['hello']
        matches = find_document_matches(self.trie, doc_contents)
        assert matches == {query_id_1, query_id_2}

        # doc_2:
        doc_id, doc_word_length, doc_contents = 2, 1, ['hell']
        matches = find_document_matches(self.trie, doc_contents)
        assert matches == set()

        # doc_3:
        doc_id, doc_word_length, doc_contents = 3, 1, ['hellox']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == set()

        # doc_4:
        doc_id, doc_word_length, doc_contents = 4, 1, ['hxllo']
        matches = find_document_matches(self.trie, doc_contents)
        assert matches == {query_id_1, query_id_2}

        # doc_5:
        doc_id, doc_word_length, doc_contents = 5, 1, ['couchix']
        matches = find_document_matches(self.trie, doc_contents)
        assert matches == {query_id_2}

        # doc_6:
        doc_id, doc_word_length, doc_contents = 6, 1, ['couchie', 'hello']
        matches = find_document_matches(self.trie, doc_contents)

        print(f"matches: {matches}")
        assert matches == {query_id_1, query_id_2}

        # doc_7:
        doc_id, doc_word_length, doc_contents = 7, 1, ['couxhie', 'helxx']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_2}

        # hamming distance 2
        self.trie.clear()

        hamming_distance = 2
        # query_1:
        query_words_1 = ['hello', "world"]
        query_id_1, query_type_1, query_dist_1, query_words_1 = 1, 1, hamming_distance, query_words_1
        input_query_in_trie(self.trie, query_id_1, query_type_1, query_dist_1, query_words_1)

        # query_2:
        query_words_2 = ['hello', "couchie"]
        query_id_2, query_type_2, query_dist_2, query_words_2 = 2, 1, hamming_distance, query_words_2
        input_query_in_trie(self.trie, query_id_2, query_type_2, query_dist_2, query_words_2)

        # doc_1:
        doc_id, doc_word_length, doc_contents = 1, 1, ['hexxo']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_1, query_id_2}

        # doc_2:
        doc_id, doc_word_length, doc_contents = 2, 1, ['cxuchxe']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_2}

        # doc_3:
        doc_id, doc_word_length, doc_contents = 3, 1, ['hell']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == set()


    def test_match_levenshtein(self):
        self._combined_exact_search(2)

        self.trie.clear()
        lev_distance = 1
        # query_1:
        query_words_1 = ['hello', "world"]
        query_id_1, query_type_1, query_dist_1, query_words_1 = 1, 2, lev_distance, query_words_1
        input_query_in_trie(self.trie, query_id_1, query_type_1, query_dist_1, query_words_1)

        # query_2:
        query_words_2 = ['hello', "couchie"]
        query_id_2, query_type_2, query_dist_2, query_words_2 = 2, 2, lev_distance, query_words_2
        input_query_in_trie(self.trie, query_id_2, query_type_2, query_dist_2, query_words_2)

        # doc_1:
        doc_id, doc_word_length, doc_contents = 1, 1, ['hexxo']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == set()

        # doc_2:
        doc_id, doc_word_length, doc_contents = 2, 1, ['cxuchxe']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == set()

        # doc_3:
        doc_id, doc_word_length, doc_contents = 3, 1, ['hell']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_1, query_id_2}

        # doc_4:
        doc_id, doc_word_length, doc_contents = 4, 1, ['hellox']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_1, query_id_2}

        # doc_4:
        doc_id, doc_word_length, doc_contents = 4, 1, ['helxlo']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_1, query_id_2}

        # doc_5:
        doc_id, doc_word_length, doc_contents = 5, 1, ['couchi']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_2}

        # doc_6:
        doc_id, doc_word_length, doc_contents = 6, 1, ['couchix']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_2}

        # doc_7:
        doc_id, doc_word_length, doc_contents = 7, 1, ['coucxhie']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_2}

        # doc_8:
        doc_id, doc_word_length, doc_contents = 7, 1, ['couxhie']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_2}

        lev_distance = 2
        self.trie.clear()

        # query_1:
        query_words_1 = ['hello', "world"]
        query_id_1, query_type_1, query_dist_1, query_words_1 = 1, 2, lev_distance, query_words_1
        input_query_in_trie(self.trie, query_id_1, query_type_1, query_dist_1, query_words_1)

        # query_2:
        query_words_2 = ['hello', "couchie"]
        query_id_2, query_type_2, query_dist_2, query_words_2 = 2, 2, lev_distance, query_words_2
        input_query_in_trie(self.trie, query_id_2, query_type_2, query_dist_2, query_words_2)

        # doc_1:
        doc_id, doc_word_length, doc_contents = 1, 1, ['hexxo']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_1, query_id_2}

        # doc_2:
        doc_id, doc_word_length, doc_contents = 2, 1, ['cxuchxe']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_2}

        # doc_4:
        doc_id, doc_word_length, doc_contents = 4, 1, ['helox']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_1, query_id_2}

        # let's start deleting or adding chars let's be really simple

        lev_distance = 1
        # doc_3:
        doc_id, doc_word_length, doc_contents = 3, 1, ['hell']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_1, query_id_2}

        # doc_5:
        doc_id, doc_word_length, doc_contents = 5, 1, ['coxchi']
        matches = find_document_matches(self.trie, doc_contents)

        assert matches == {query_id_2}

        # doc_6:
        doc_id, doc_word_length, doc_contents = 6, 1, ['ouxhiex']
        matches = find_document_matches(self.trie, doc_contents)

        print(f"matches: {matches}")
        assert matches == set()

        lev_distance = 2
        # query_3:
        query_words_3 = ['hello', "world"]
        query_id_3, query_type_3, query_dist_3, query_words_3 = 3, 2, lev_distance, query_words_3
        input_query_in_trie(self.trie, query_id_3, query_type_3, query_dist_3, query_words_3)



if __name__ == '__main__':
    unittest.main()