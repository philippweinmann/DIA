# %%
import itertools
from enum import Enum
from bitarray import bitarray

class MatchType(Enum):
    EXACT = 0
    EDIT = 2
    HAMMING = 1

# add caching!
# %%

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

# %

def get_deletion(word, mask):
    mask = bitarray(mask)
    return "".join([letter for letter, keep in zip(word, mask) if keep == 0])

# %%
def get_deletions_for_document(words, max_dist):
    word_mask_tuples = set()
    for original_word in words:
        combinations = generate_combinations(len(original_word), max_dist)
        for mask in combinations:
            word_mask_tuples.add((get_deletion(original_word, mask), mask, original_word))
    
    return word_mask_tuples

# %%
def get_trie_inputs(query_id, query_type, query_dist, query_words):
    trie_inputs = []

    word_tuples = get_deletions_for_document(query_words, max_dist=query_dist)
    for word, mask, original_word in word_tuples:
        trie_inputs.append((word, (query_id, query_type, query_dist, mask, original_word)))
    return trie_inputs

# I'll just assime this works
# %%
def input_query_in_trie(trie, query_id, query_type, query_dist, query_words):
    query_inputs = get_trie_inputs(query_id, query_type, query_dist, query_words)
    for word, query_info in query_inputs:
        value = trie.get(word, None)
        if not value:
            trie[word] = [query_info]
        else:
            value.append(query_info)

# %%
def delete_query_from_trie(trie, query_id, query_keys):
    for word in query_keys:
        value = trie.get(word, None)
        if value:
            value.remove(query_id)
            if not value:
                del trie[word]
# %%

def pad_bitarrays(doc_mask, query_mask):
    """
    Pad the shorter mask with 0 (False) bits so that doc_mask and query_mask 
    end up having the same length. Return (padded_doc_mask, padded_query_mask).
    """
    doc_len_diff = len(doc_mask) - len(query_mask)

    if doc_len_diff > 0:
        # doc_mask is longer; pad query_mask
        zero_bits = bitarray(doc_len_diff)
        zero_bits.setall(False)
        padded_doc_mask = doc_mask
        padded_query_mask = zero_bits + query_mask
    elif doc_len_diff < 0:
        # query_mask is longer; pad doc_mask
        zero_bits = bitarray(-doc_len_diff)
        zero_bits.setall(False)
        padded_doc_mask = zero_bits + doc_mask
        padded_query_mask = query_mask
    else:
        # They are already equal length
        padded_doc_mask = doc_mask
        padded_query_mask = query_mask

    return padded_doc_mask, padded_query_mask

def find_word_in_trie(trie, word, mask):
    query_infos = trie.get(word, None)
    mask = bitarray(mask)

    if not query_infos:
        return []
    
    matching_queries = set()
    for query_info in query_infos:
        query_id, query_type, query_dist, query_mask, original_word = query_info
        query_mask = bitarray(query_mask)

        match MatchType(query_type):
            case MatchType.EXACT:
                if mask.count(1) != 0:
                    continue
                if mask == query_mask:
                    matching_queries.add((query_id, original_word))
            case MatchType.HAMMING:
                if mask != query_mask:
                    continue
                if mask.count(1) <= query_dist:
                    matching_queries.add((query_id, original_word))
            case MatchType.EDIT:
                '''
                # compare mask lengths and pad at the start to make them equal
                mask_len_diff = len(mask) - len(query_mask)

                if mask_len_diff > 0:
                    query_mask = [0] * mask_len_diff + query_mask
                elif mask_len_diff < 0:
                    mask = [0] * abs(mask_len_diff) + mask
                
                # count amount of 1s as nand of the two masks
                lev_dist = sum([1 for a, b in zip(mask, query_mask) if a != b])

                if lev_dist <= query_dist:
                    matching_queries.add(query_id)
                
                '''
                padded_doc_mask, padded_query_mask = pad_bitarrays(mask, query_mask)
                
                # I believe they should always have the same length
                assert len(padded_doc_mask) == len(padded_query_mask)
                # nand counter for the two bitarrays
                lev_dist = (padded_doc_mask | padded_query_mask).count(1)

                # this needs to be the last check
                if lev_dist <= query_dist:
                    matching_queries.add((query_id, original_word))
            
    return matching_queries

def find_document_matches(trie, doc_words, reference_queries):
    # max distance is 3
    found_query_words_dict = {key: set() for key in reference_queries}

    doc_matches = set()
    for original_word in doc_words:
        word_mask_tuples = get_deletions_for_document([original_word], max_dist=3)
        for deleted_word_comb, mask, original_word in word_mask_tuples:
            results = find_word_in_trie(trie, deleted_word_comb, mask)
            # found_query_id, query_word
            # here we need to check if allwords in query have been found.

            if results:
                for results in results:
                    found_query_id, query_word = results[0], results[1]
                    found_query_words_dict[found_query_id].add(query_word)
            
    # add only if all words in the query have been found
    for query_id, query_words in found_query_words_dict.items():
        if len(query_words) == len(reference_queries[query_id]["terms"]):
            doc_matches.add(query_id)

    return doc_matches

# %%
