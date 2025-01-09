# we simply overwrite some functions from max_throughput_core.py and reference_core.py in dask_core.py
from core_utils import ErrorCode
from max_throughput_core import MaxThroughputCore
from dask_utils import find_document_matches_dask

class DaskCore(MaxThroughputCore):
    def match_document(self, doc_id, content):
        """
        Matches a document against all active queries and stores the result if matched.
        """
        trie_matches = list(find_document_matches_dask(self.trie, content.split(), self.queries))
        self.results.append((doc_id, trie_matches))
        
        return ErrorCode.EC_SUCCESS