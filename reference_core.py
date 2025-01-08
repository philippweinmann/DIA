from abstract_core import AbstractCore
from core_utils import MatchType, ErrorCode

queries = {}  # Stores active queries
results = []  # Stores matched results for retrieval

# implementation for 1.1
class ReferenceCore(AbstractCore):
    def __init__(self):
        self.queries = {}
        self.results = []

    def initialize_index(self):
        """
        Clears all queries and results to initialize the indexing system.
        """
        self.queries.clear()
        self.results.clear()

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

        # Store query information
        self.queries[query_id] = {
            'terms': terms.split(),
            'match_type': MatchType(match_type),
            'match_dist': match_dist
        }
        return ErrorCode.EC_SUCCESS
    
    def end_query(self, query_id):
        """
        Ends a query by removing it from the active query list.
        """
        if query_id not in self.queries:
            return ErrorCode.EC_FAIL
        del self.queries[query_id]
        return ErrorCode.EC_SUCCESS
    
    def match_document(self, doc_id, content):
        """
        Matches a document against all active queries and stores the result if matched.
        """
        matched_queries = []

        for query_id, query in self.queries.items():
            if self.matches_query(query, content):
                matched_queries.append(query_id)

        if matched_queries:
            self.results.append((doc_id, matched_queries))
        return ErrorCode.EC_SUCCESS

    def get_next_avail_res(self):
        """
        Retrieves the next available result for delivery.
        """
        if not self.results:
            return ErrorCode.EC_NO_AVAIL_RES, None, None, None

        doc_id, matched_queries = self.results.pop(0)
        return ErrorCode.EC_SUCCESS, doc_id, len(matched_queries), matched_queries
    
    def matches_query(self, query, content):
        terms = query['terms']
        match_type = query['match_type']
        match_dist = query['match_dist']
        
        # Split document content into terms
        doc_terms = content.split()
        
        # Iterate over each query term
        for term in terms:
            matching_word = False  
            
            # Check each document term to find a match based on the match type
            for doc_term in doc_terms:
                if match_type == MatchType.EXACT:
                    if term == doc_term:
                        matching_word = True
                        break
                
                elif match_type == MatchType.EDIT:
                    dist = self.edit_distance(term, doc_term)
                    if dist <= match_dist:
                        matching_word = True
                        break
                
                elif match_type == MatchType.HAMMING:
                    dist = self.hamming_distance(term, doc_term)
                    if dist <= match_dist:
                        matching_word = True
                        break

            
            if not matching_word:
                return False
        
        return True
    
    def edit_distance(self, s1, s2):
        len_s1, len_s2 = len(s1), len(s2)
        if len_s1 == 0:
            return len_s2
        if len_s2 == 0:
            return len_s1

        # Create a full 2D DP table 
        dp_table = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

        # Initialize the base cases
        for i in range(len_s1 + 1):
            dp_table[i][0] = i
        for j in range(len_s2 + 1):
            dp_table[0][j] = j

        # Fill the DP table
        for i in range(1, len_s1 + 1):
            for j in range(1, len_s2 + 1):
                insert_cost = dp_table[i - 1][j] + 1
                delete_cost = dp_table[i][j - 1] + 1
                replace_cost = dp_table[i - 1][j - 1]
                if s1[i - 1] != s2[j - 1]:
                    replace_cost += 1
                dp_table[i][j] = min(insert_cost, delete_cost, replace_cost)

        return dp_table[len_s1][len_s2]
    
    def hamming_distance(self, s1, s2):
        if len(s1) != len(s2):
            return 0x7FFFFFFF  

        return sum(1 for x, y in zip(s1, s2) if x != y)