import pygtrie

from trie_utils import input_query_in_trie, delete_query_from_trie, find_document_matches
from core_utils import MatchType, ErrorCode

# storing queries is still necessary, even if we have the trie,
#  to check if all words in a query have been found
queries = {}  # Stores active queries
results = []  # Stores matched results for retrieval
trie = pygtrie.CharTrie() # global chartrie for all queries

# Initialize the indexing system
def initialize_index():
    """
    Clears all queries and results to initialize the indexing system.
    """
    global queries, results, trie
    queries.clear()
    results.clear()
    trie = pygtrie.CharTrie()


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
    queries[query_id] = {
        'terms': terms,
        'match_type': MatchType(match_type),
        'match_dist': match_dist
    }

    input_query_in_trie(trie, query_id, match_type, match_dist, terms)
    return ErrorCode.EC_SUCCESS


def end_query(query_id):
    """
    Ends a query by removing it from the active query list.
    """
    terms, match_type, match_dist = queries[query_id]['terms'], queries[query_id]['match_type'], queries[query_id]['match_dist']
    delete_query_from_trie(trie, query_id, terms, match_type, match_dist)
    
    # this should never happen
    if query_id not in queries:
        return ErrorCode.EC_FAIL
    
    del queries[query_id]
    
    return ErrorCode.EC_SUCCESS


def match_document(doc_id, content):
    """
    Matches a document against all active queries and stores the result if matched.
    """
    trie_matches = list(find_document_matches(trie, content.split(), queries))
    results.append((doc_id, trie_matches))
    
    return ErrorCode.EC_SUCCESS


def get_next_avail_res():
    """
    Retrieves the next available result for delivery.
    """
    if not results:
        return ErrorCode.EC_NO_AVAIL_RES, None, None, None

    doc_id, matched_queries = results.pop(0)

    matched_queries = set(matched_queries)
    return ErrorCode.EC_SUCCESS, doc_id, len(matched_queries), matched_queries
