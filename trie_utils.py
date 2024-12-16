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
    for word in words:
        combinations = generate_combinations(len(word), max_dist)
        for mask in combinations:
            word_mask_tuples.add((get_deletion(word, mask), mask))
    
    return word_mask_tuples

# %%
def get_trie_inputs(query_id, query_type, query_dist, query_words):
    trie_inputs = []

    word_tuples = get_deletions_for_document(query_words, max_dist=query_dist)
    for word, mask in word_tuples:
        trie_inputs.append((word, (query_id, query_type, query_dist, mask)))
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
def pad_bitarrays(doc_mask: bitarray, query_mask: bitarray):
    padded_doc_mask = bitarray()
    padded_query_mask = bitarray()
    
    # Iterate through the bitarrays, extending the result bitarrays as needed
    for bit_a, bit_b in zip(doc_mask, query_mask):
        if bit_a == 1 and bit_b == 0:
            padded_doc_mask.extend([0, 1])
            padded_query_mask.extend([0, 0])
        elif bit_b == 1 and bit_a == 0:
            padded_doc_mask.extend([0, 0])
            padded_query_mask.extend([0, 1])
        else:
            padded_doc_mask.append(bit_a)
            padded_query_mask.append(bit_b)
    
    return padded_doc_mask, padded_query_mask

def find_word_in_trie(trie, word, mask):
    query_infos = trie.get(word, None)
    mask = bitarray(mask)

    if not query_infos:
        return []
    
    matching_queries = set()
    for query_info in query_infos:
        query_id, query_type, query_dist, query_mask = query_info
        query_mask = bitarray(query_mask)

        match MatchType(query_type):
            case MatchType.EXACT:
                if mask.count(1) != 0:
                    continue
                if mask == query_mask:
                    matching_queries.add(query_id)
            case MatchType.HAMMING:
                if mask != query_mask:
                    continue
                if mask.count(1) <= query_dist:
                    matching_queries.add(query_id)
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
                    matching_queries.add(query_id)
            
    return matching_queries

def find_document_matches(trie, doc_words):
    # max distance is 3

    doc_matches = set()
    for original_word in doc_words:
        word_mask_tuples = get_deletions_for_document([original_word], max_dist=3)
        for deleted_word_comb, mask in word_mask_tuples:
            doc_matches.update(find_word_in_trie(trie, deleted_word_comb, mask))
    return doc_matches

# %%
