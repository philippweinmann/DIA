import unittest
from main import QueryManager
from pathlib import Path

class TestSigmoid(unittest.TestCase):
    small_test_fp = Path("data/small_test.txt")

    def test_exact_matches(self):
        print("Start Test ...\n")

        query_manager = QueryManager()
        query_manager.start_query(query_id=1, query_text="data integration", match_type="exact", match_distance=0)
        query_manager.end_query(query_id=1)

        with open(self.small_test_fp, "r") as f:
            
        


if __name__ == '__main__':
    unittest.main()