from enum import Enum
import functools


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

# Initialize the indexing system
def initialize_index():
    """
    Clears all queries and results to initialize the indexing system.
    """
    global queries, results
    queries.clear()
    results.clear()


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

    # Store query information
    queries[query_id] = {
        'terms': terms.split(),
        'match_type': MatchType(match_type),
        'match_dist': match_dist
    }
    return ErrorCode.EC_SUCCESS


def end_query(query_id):
    """
    Ends a query by removing it from the active query list.
    """
    if query_id not in queries:
        return ErrorCode.EC_FAIL
    del queries[query_id]
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
                dist = cached_edit_distance(term, doc_term)
                if dist <= match_dist:
                    matching_word = True
                    break  

            elif match_type == MatchType.HAMMING:
                dist = cached_hamming_distance(term, doc_term)
                if dist <= match_dist:
                    matching_word = True
                    break  
        
        if not matching_word:
            return False
    
    return True


# Caching-enhanced distance functions
@functools.lru_cache(maxsize=None)
def cached_edit_distance(s1, s2):
    """
    Calculates the edit distance between two strings, optimized with dynamic programming.
    """
    len_s1, len_s2 = len(s1), len(s2)
    if len_s1 == 0:
        return len_s2
    if len_s2 == 0:
        return len_s1

    prev_row = list(range(len_s2 + 1))
    curr_row = [0] * (len_s2 + 1)

    for i in range(1, len_s1 + 1):
        curr_row[0] = i
        for j in range(1, len_s2 + 1):
            insert_cost = prev_row[j] + 1
            delete_cost = curr_row[j - 1] + 1
            replace_cost = prev_row[j - 1]
            if s1[i - 1] != s2[j - 1]:
                replace_cost += 1
            curr_row[j] = min(insert_cost, delete_cost, replace_cost)
        
        prev_row, curr_row = curr_row, prev_row

    return prev_row[len_s2]


@functools.lru_cache(maxsize=None)
def cached_hamming_distance(s1, s2):
    """
    Calculates the Hamming distance between two strings of the same length, with caching.
    If lengths differ, returns a large integer penalty.
    """
    if len(s1) != len(s2):
        return 0x7FFFFFFF  

    return sum(1 for x, y in zip(s1, s2) if x != y)
