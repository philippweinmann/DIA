import unittest
from main import QueryManager

class TestSigmoid(unittest.TestCase):
    def test_something(self):
        print("Start Test ...\n")

        query_manager = QueryManager()
        query_manager.start_query(query_id=1, query_text="data integration", match_type="exact", match_distance=0)
        query_manager.end_query(query_id=1)

if __name__ == '__main__':
    unittest.main()