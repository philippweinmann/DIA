from abstract_core import AbstractCore
import pygtrie

from trie_utils import input_query_in_trie, delete_query_from_trie, find_document_matches
from core_utils import MatchType, ErrorCode

# Implementation for 1.2
class MaxThroughputCore(AbstractCore):
    def __init__(self):
        self.queries = {}
        self.results = []
        self.trie = pygtrie.CharTrie()

    def initialize_index(self):
        """
        Clears all queries and results to initialize the indexing system.
        """
        self.queries.clear()
        self.results.clear()
        self.trie = pygtrie.CharTrie()

    def destroy_index(self):
        """
        Clears the index, effectively the same as re-initializing.
        """
        self.initialize_index()

    def start_query(self, query_id, terms, match_type, match_dist):
        """
        Initializes a new query with the specified id, terms, match type, and distance.
        """
        if query_id in self.queries:
            return ErrorCode.EC_FAIL
        
        terms = terms.split()
        self.queries[query_id] = {
            'terms': terms,
            'match_type': MatchType(match_type),
            'match_dist': match_dist
        }

        input_query_in_trie(self.trie, query_id, match_type, match_dist, terms)
        return ErrorCode.EC_SUCCESS
    
    def end_query(self, query_id):
        """
        Ends a query by removing it from the active query list.
        """
        terms, match_type, match_dist = self.queries[query_id]['terms'], self.queries[query_id]['match_type'], self.queries[query_id]['match_dist']
        delete_query_from_trie(self.trie, query_id, terms, match_type, match_dist)
        
        if query_id not in self.queries:
            return ErrorCode.EC_FAIL
        
        del self.queries[query_id]
        
        return ErrorCode.EC_SUCCESS
    
    def match_document(self, doc_id, content):
        """
        Matches a document against all active queries and stores the result if matched.
        """
        trie_matches = list(find_document_matches(self.trie, content.split(), self.queries))
        self.results.append((doc_id, trie_matches))
        
        return ErrorCode.EC_SUCCESS
    
    def get_next_avail_res(self):
        """
        Retrieves the next available result for delivery.
        """
        if not self.results:
            return ErrorCode.EC_NO_AVAIL_RES, None, None, None

        doc_id, matched_queries = self.results.pop(0)

        matched_queries = set(matched_queries)
        return ErrorCode.EC_SUCCESS, doc_id, len(matched_queries), matched_queries