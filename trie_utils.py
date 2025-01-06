# %%
import itertools
from core_utils import MatchType
from bitarray import bitarray
from functools import lru_cache

lev_dist_dict = {}

@lru_cache(maxsize=None)
def calculate_levenshtein_distance_with_bitmask(barray_str_1, barray_str_2):
    barray_1 = bitarray(barray_str_1)
    barray_2 = bitarray(barray_str_2)

    start_index = 0
    l1 = len(barray_1)
    l2 = len(barray_2)


    while start_index < min(l1, l2):
        bit1 = barray_1[start_index]
        bit2 = barray_2[start_index]

        if bit1 == bit2:
            start_index += 1
        elif bit2: # bit2 is 1
            barray_1.insert(start_index, 0)
            start_index += 1
            l1 += 1
        elif bit1: # bit1 is 1
            barray_2.insert(start_index, 0)
            start_index += 1
            l2 += 1
        else:
            print(f"Error: {barray_1} {barray_2}, start_index={start_index}")

    # only the trailing ones are left
    ldiff = l1 - l2
    if ldiff > 0:
        barray_2.extend('0' * ldiff)
    elif ldiff < 0:
        barray_1.extend('0' * -ldiff)
    
    barray_1 |= barray_2

    lev_dist = barray_1.count()

    global lev_dist_dict
    lev_dist_dict[(barray_str_1, barray_str_2)] = lev_dist

    return lev_dist
# %%
@lru_cache(maxsize=None)
def generate_combinations(array_length, max_ones):
    result = set()
    # Add the all-zero mask as a string
    result.add("0" * array_length)
    for num_ones in range(1, max_ones + 1):
        for indices in itertools.combinations(range(array_length), num_ones):
            bitar = ["0"] * array_length
            for index in indices:
                bitar[index] = "1"
            # Add the string representation of the bitarray
            result.add("".join(bitar))
    return result

def get_deletion(word, mask):
    mask = bitarray(mask)
    return "".join([letter for letter, keep in zip(word, mask) if keep == 0])

def get_deletions_for_document(words, max_dist):
    word_mask_tuples = set()
    for original_word in words:
        combinations = generate_combinations(len(original_word), max_dist)
        for mask in combinations:
            word_mask_tuples.add((get_deletion(original_word, mask), mask, original_word))
    
    return word_mask_tuples

def get_trie_inputs(query_id, query_type, query_dist, query_words):
    trie_inputs = []

    word_tuples = get_deletions_for_document(query_words, max_dist=query_dist)
    for word, mask, original_word in word_tuples:
        trie_inputs.append((word, (query_id, query_type, query_dist, mask, original_word)))
    return trie_inputs

def input_query_in_trie(trie, query_id, query_type, query_dist, query_words):
    query_inputs = get_trie_inputs(query_id, query_type, query_dist, query_words)
    for word, query_info in query_inputs:
        value = trie.get(word, None)
        if not value:
            trie[word] = [query_info]
        else:
            value.append(query_info)

def delete_query_from_trie(trie, query_id, terms, match_type, match_dist):
    query_inputs = get_trie_inputs(query_id, match_type, match_dist, terms)
    for word, query_info in query_inputs:
        value = trie[word] # it is garanteed to exist
        # remove only the query that matches the query_id
        trie[word] = [query for query in value if query[0] != query_id]

@lru_cache(maxsize=None)
def check_exact_match(document_mask_str, query_mask_str):
    return document_mask_str == query_mask_str

@lru_cache(maxsize=None)
def get_hamming_distance(document_mask_str, query_mask_str):
    if document_mask_str != query_mask_str:
        return 4  # 4 is bigger than any possible distance

    return document_mask_str.count('1')

def find_word_in_trie(trie, word, document_mask_str):
    query_infos = trie.get(word, None)

    if not query_infos:
        return []
    
    matching_queries = set()
    for query_info in query_infos:
        query_id, query_type, query_dist, query_mask_str, original_query_word = query_info

        match MatchType(query_type):
            case MatchType.EXACT:
                if check_exact_match(document_mask_str, query_mask_str):
                    matching_queries.add((query_id, original_query_word))
            case MatchType.HAMMING:
                if get_hamming_distance(document_mask_str, query_mask_str) <= query_dist:
                    matching_queries.add((query_id, original_query_word))

            case MatchType.EDIT:
                lev_dist = calculate_levenshtein_distance_with_bitmask(document_mask_str, query_mask_str)

                if lev_dist <= query_dist:
                    matching_queries.add((query_id, original_query_word))
            
    return matching_queries

def find_document_matches(trie, doc_words, reference_queries):
    found_query_words_dict = {key: set() for key in reference_queries}

    doc_matches = set()
    for original_word in doc_words:
        # no query has distance above 3
        doc_word_mask_tuples = get_deletions_for_document([original_word], max_dist=3)
        for doc_deleted_word_comb, mask, original_word in doc_word_mask_tuples:
            results = find_word_in_trie(trie, doc_deleted_word_comb, mask)
            
            # now we need to check if all words in query have been found.
            if results:
                for results in results: # found_query_id, query_word
                    found_query_words_dict[results[0]].add(results[1])
            
    # add match only if all words in the query have been found
    for query_id, query_words in found_query_words_dict.items():
        if len(query_words) == len(reference_queries[query_id]["terms"]):
            doc_matches.add(query_id)

    return doc_matches

# %%
