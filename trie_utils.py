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

    for dist in range(1, query_dist + 1):
        mask_word_tuples = get_deletions_for_document(query_words, max_dist=dist)
        for word, mask in mask_word_tuples:
            trie_inputs.append((word, (query_id, query_type, query_dist, mask)))
    return trie_inputs

# I'll just assime this works
# %%

