# Define the data structure to store active queries
class QueryManager:
    def __init__(self):
        # Dictionary to hold active queries with their details
        self.active_queries = {}

    def start_query(self, query_id, keywords, match_type="exact", match_distance=0):
        if query_id in self.active_queries:
            raise ValueError(f"Query ID {query_id} already exists in active queries.")
        
        # Add query to active queries with specified matching type and distance
        self.active_queries[query_id] = {
            'keywords': keywords,
            'match_type': match_type,
            'match_distance': match_distance
        }

# Example usage
# query_manager = QueryManager()
# query_manager.start_query(query_id=1, keywords="data integration", match_type="edit", match_distance=2)
