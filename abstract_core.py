# We have to implement the same functions in three different ways.
# therefore we should use abstract classes to define the core functions and then implement them in the three different ways.

from abc import ABC, abstractmethod

class AbstractCore(ABC):
    @abstractmethod
    def initialize_index(self):
        """
        Clears all queries and results to initialize the indexing system.
        """
        pass

    @abstractmethod
    def destroy_index(self):
        """
        Clears the index, effectively the same as re-initializing.
        """
        pass

    @abstractmethod
    def start_query(self, query_id, terms, match_type, match_dist):
        """
        Initializes a new query with the specified id, terms, match type, and distance.
        """
        pass

    @abstractmethod
    def end_query(self, query_id):
        """
        Ends a query by removing it from the active query list.
        """
        pass

    @abstractmethod
    def match_document(self, doc_id, content):
        """
        Matches a document against all active queries and stores the result if matched.
        """
        pass