# %%
import itertools

# add caching!
# %%
def generate_combinations(array_length, max_ones):
    result = set()
    # manually add the all-zero mask
    result.add(tuple([0] * array_length))
    for num_ones in range(1, max_ones + 1):
        for indices in itertools.combinations(range(array_length), num_ones):
            array = [0] * array_length
            for index in indices:
                array[index] = 1
            result.add(tuple(array))
    return result
# %

def get_deletion(word, mask):
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
import pygtrie
from lorem_text import lorem

t = pygtrie.CharTrie()

query_1 = (1, 1, 2, ["hello", "world"])
query_2 = (2, 1, 3, ["hello", "cruel"])

input_query_in_trie(t, *query_1)
input_query_in_trie(t, *query_2)

# use t.get(word, None) to get the list of queries