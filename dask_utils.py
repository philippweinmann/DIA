# the overhead from the imports alone is so high that it's worth it to put them in a separate file
from dask import delayed, compute

from trie_utils import find_partial_document_matches, combine_partial_document_matches

def find_document_matches_dask(trie, doc_words, reference_queries):
    # the results from the combined ones are a list, so we're just mocking that behaviour here.
    num_cores = 4

    partial_doc_words = [doc_words[i::num_cores] for i in range(num_cores)]
    inputs = [(trie, partial_doc_word, reference_queries) for partial_doc_word in partial_doc_words]

    partial_found_query_words_dicts = [delayed(find_partial_document_matches(input)) for input in inputs]

    # let's compute it all in parallel:
    partial_found_query_words_dicts = compute(*partial_found_query_words_dicts)

    doc_matches = combine_partial_document_matches(partial_found_query_words_dicts, reference_queries)

    return doc_matches