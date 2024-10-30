class QueryManager:
    def __init__(self):
        self.active_queries = {}

    # keywords is equivalent to char str[MAX_QUERY_LENGTH]; in c++
    def start_query(self, query_id, query_text, match_type="exact", match_distance=0):
        if query_id in self.active_queries:
            raise ValueError(f"Query ID {query_id} already exists in active queries.")
        
        # Add query to active queries with specified matching type and distance
        self.active_queries[query_id] = {
            'query_text': query_text,
            'match_type': match_type,
            'match_distance': match_distance
        }

    def end_query(self, query_id):
        if query_id in self.active_queries:
            del self.active_queries[query_id]

    def MatchDocument(self, doc_id, doc_str: str):
        for query in self.active_queries:

            pass
        

# Example usage
# query_manager = QueryManager()
# query_manager.start_query(query_id=1, keywords="data integration", match_type="edit", match_distance=2)
