# core.py

from enum import Enum
import re

# Define error codes
class ErrorCode(Enum):
    EC_SUCCESS = 0
    EC_FAIL = 1
    EC_NO_AVAIL_RES = 2

# Define MatchType enumeration to match C++ structure
class MatchType(Enum):
    EXACT = 0
    EDIT = 2
    HAMMING = 1

# Data structures for storing queries and documents
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

# Cleanup function for the indexing system
def destroy_index():
    """
    Clears the index, effectively the same as re-initializing.
    """
    initialize_index()

# Core function definitions
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
    print(f"Added query {query_id} with terms: {terms}, match_type: {match_type}, match_dist: {match_dist}")
    print(f"Current queries: {queries}")
    return ErrorCode.EC_SUCCESS

def end_query(query_id):
    """
    Ends a query by removing it from the active query list.
    """
    if query_id not in queries:
        return ErrorCode.EC_FAIL
    del queries[query_id]
    print(f"Removed query {query_id}. Current queries after deletion: {queries}")

    return ErrorCode.EC_SUCCESS

def match_document(doc_id, content):
    """
    Matches a document against all active queries and stores the result if matched.
    """
    matched_queries = []

    for query_id, query in queries.items():
        if matches_query(query, content):
            matched_queries.append(query_id)
            print(f"Query {query_id} matched with Document {doc_id}")
        else:
            print(f"Query {query_id} did NOT match with Document {doc_id}")


    if matched_queries:
        results.append((doc_id, matched_queries))
        print(f"Document {doc_id} matched with queries: {matched_queries}")
    print(f"Results list after matching document {doc_id}: {results}")
    return ErrorCode.EC_SUCCESS

def get_next_avail_res():
    """
    Retrieves the next available result for delivery.
    """
    if not results:
        print("No available results in results list.")
        return ErrorCode.EC_NO_AVAIL_RES, None, None, None

    doc_id, matched_queries = results.pop(0)
    print(f"Retrieved next result: Doc ID={doc_id}, Num Res={len(matched_queries)}, Query IDs={matched_queries}")
    print(f"Results list after retrieval: {results}")
    return ErrorCode.EC_SUCCESS, doc_id, len(matched_queries), matched_queries

# Helper functions for matching logic
def matches_query(query, content):
    terms = query['terms']
    match_type = query['match_type']
    match_dist = query['match_dist']

    for term in terms:
        if match_type == MatchType.EXACT:
            match = term in content
            
            if not match:
                return False
        elif match_type == MatchType.EDIT:
            dist = edit_distance(term, content)
            
            if dist > match_dist:
                return False
        elif match_type == MatchType.HAMMING:
            for doc_term in content.split():  # or however you break the document content into terms
                dist = hamming_distance(term, doc_term)
                #print(f"Hamming Distance Check - Term: {term}, Document Term: {doc_term}, Distance: {dist}, Threshold: {match_dist}")
                if dist <= match_dist:
                    return True  # Match found within threshold, stop checking further terms
            return False  # No match found within threshold after checking all terms

    return True


# Function to calculate edit distance
def edit_distance(s1, s2):
    """
    Calculates the Levenshtein distance (edit distance) between two strings.
    """
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        dp[i][0] = i
    for j in range(len_s2 + 1):
        dp[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + 1)

    return dp[len_s1][len_s2]

# Function to calculate Hamming distance
def hamming_distance(s1, s2):
    """
    Calculates the Hamming distance between two strings of the same length.
    If lengths differ, returns a large integer penalty (matching C++ behavior).
    """
    if len(s1) != len(s2):
        return 0x7FFFFFFF  # Large penalty for differing lengths, matching C++ value

    return sum(1 for x, y in zip(s1, s2) if x != y)

