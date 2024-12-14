from enum import Enum
import functools
from rapidfuzz.distance import Hamming, Levenshtein
import pygtrie

from trie_utils import input_query_in_trie, delete_query_from_trie, find_document_matches


class ErrorCode(Enum):
    EC_SUCCESS = 0
    EC_FAIL = 1
    EC_NO_AVAIL_RES = 2


class MatchType(Enum):
    EXACT = 0
    EDIT = 2
    HAMMING = 1


queries = {}  # Stores active queries
results = []  # Stores matched results for retrieval
t = pygtrie.CharTrie() # global chartrie for all queries

# Initialize the indexing system
def initialize_index():
    """
    Clears all queries and results to initialize the indexing system.
    """
    global queries, results, t
    queries.clear()
    results.clear()
    t = pygtrie.CharTrie()


def destroy_index():
    """
    Clears the index, effectively the same as re-initializing.
    """
    initialize_index()


def start_query(query_id, terms, match_type, match_dist):
    """
    Initializes a new query with the specified id, terms, match type, and distance.
    """
    if query_id in queries:
        return ErrorCode.EC_FAIL  # Query ID already exists

    terms = terms.split()
    # Store query information
    queries[query_id] = {
        'terms': terms,
        'match_type': MatchType(match_type),
        'match_dist': match_dist
    }

    # Insert query into trie
    input_query_in_trie(t, query_id, match_type, match_dist, terms)
    return ErrorCode.EC_SUCCESS


def end_query(query_id):
    """
    Ends a query by removing it from the active query list.
    """
    if query_id not in queries:
        return ErrorCode.EC_FAIL
    del queries[query_id]

    # Remove query from trie
    delete_query_from_trie(t, query_id, queries[query_id])
    return ErrorCode.EC_SUCCESS


def match_document(doc_id, content):
    """
    Matches a document against all active queries and stores the result if matched.
    """
    matched_queries = []

    for query_id, query in queries.items():
        if matches_query(query, content):
            matched_queries.append(query_id)
            # print(f"Query {query_id} matched with Document {doc_id}")
        # else:
            # print(f"Query {query_id} did NOT match with Document {doc_id}")


    if matched_queries:
        results.append((doc_id, matched_queries))
        # print(f"Document {doc_id} matched with queries: {matched_queries}")
    # print(f"Results list after matching document {doc_id}: {results}")
    
    trie_matches = list(find_document_matches(t, content.split()))
    print(f"Trie matches for document    {doc_id}: {trie_matches}")
    print(f"Matched queries for document {doc_id}: {matched_queries}")
    return ErrorCode.EC_SUCCESS


def get_next_avail_res():
    """
    Retrieves the next available result for delivery.
    """
    if not results:
        return ErrorCode.EC_NO_AVAIL_RES, None, None, None

    doc_id, matched_queries = results.pop(0)
    return ErrorCode.EC_SUCCESS, doc_id, len(matched_queries), matched_queries


# Helper functions for matching logic
def matches_query(query, content):
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
                if get_edit_distance(term, doc_term) <= match_dist:
                    matching_word = True
                    break

            elif match_type == MatchType.HAMMING:
               if get_hamming_distance(term, doc_term) <= match_dist:
                    matching_word = True
                    break
        
        if not matching_word:
            return False
    
    return True


# Caching-enhanced distance functions
@functools.lru_cache(maxsize=None)
def get_edit_distance(s1, s2):
    """
    Calculates the edit distance between two strings, optimized with dynamic programming.
    """
    return Levenshtein.distance(s1, s2)


@functools.lru_cache(maxsize=None)
def get_hamming_distance(s1, s2):
    """
    Calculates the Hamming distance between two strings of the same length, with caching.
    If lengths differ, returns a large integer penalty.
    """
    if len(s1) != len(s2):
        return 0x7FFFFFFF  

    return Hamming.distance(s1, s2, pad=False)
