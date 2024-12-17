from enum import Enum
from core_utils import MatchType, ErrorCode

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
    # print(f"Added query {query_id} with terms: {terms}, match_type: {match_type}, match_dist: {match_dist}")
    # print(f"Current queries: {queries}")
    return ErrorCode.EC_SUCCESS

def end_query(query_id):
    """
    Ends a query by removing it from the active query list.
    """
    if query_id not in queries:
        return ErrorCode.EC_FAIL
    del queries[query_id]
    # print(f"Removed query {query_id}. Current queries after deletion: {queries}")

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
        print("No available results in results list.")
        return ErrorCode.EC_NO_AVAIL_RES, None, None, None

    doc_id, matched_queries = results.pop(0)
    # print(f"Retrieved next result: Doc ID={doc_id}, Num Res={len(matched_queries)}, Query IDs={matched_queries}")
    # print(f"Results list after retrieval: {results}")
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
                    break  # Exit the loop if an exact match is found
                # print(f"Exact Match Check - Term: {term}, Document Term: {doc_term} -> No Match")

            elif match_type == MatchType.EDIT:
                dist = edit_distance(term, doc_term)
                # print(f"Edit Distance Check - Term: {term}, Document Term: {doc_term}, Distance: {dist}, Threshold: {match_dist}")
                if dist <= match_dist:
                    matching_word = True
                    break  

            elif match_type == MatchType.HAMMING:
                dist = hamming_distance(term, doc_term)
                # print(f"Hamming Distance Check - Term: {term}, Document Term: {doc_term}, Distance: {dist}, Threshold: {match_dist}")
                if dist <= match_dist:
                    matching_word = True
                    break  
        
        
        if not matching_word:
            # print(f"Query term '{term}' did NOT match any document term.")
            return False
    
    return True




def edit_distance(s1, s2):
    """
    Calculates the edit distance between two strings using a 2D array.
    """
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




def hamming_distance(s1, s2):
    """
    Calculates the Hamming distance between two strings of the same length.
    If lengths differ, returns a large integer penalty (matching C++ behavior).
    """
    if len(s1) != len(s2):
        return 0x7FFFFFFF  

    return sum(1 for x, y in zip(s1, s2) if x != y)

