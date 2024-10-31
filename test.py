import unittest
from main import QueryManager, CommandType
from pathlib import Path
from enum import Enum

command = {
    "s": CommandType.START_QUERY,
    "e": CommandType.END_QUERY,
    "r": CommandType.GET_NEXT_RES,
    "m": CommandType.MATCH_DOCUMENT,
}

class command_regex_parse(Enum):
    CommandType.START_QUERY: r"^s\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s([a-zA-Z]+)\s(.*)$",
    CommandType.END_QUERY: r"^e\s(\d+)$",
    CommandType.GET_NEXT_RES: r"",

class TestSigmoid(unittest.TestCase):
    small_test_fp = Path("data/small_test.txt")

    def _get_next_element_in_line(self, line, start_idx):
        end_idx = line.find(" ", start_idx)
        if end_idx == -1:
            end_idx = len(line)
        return line[start_idx:end_idx], end_idx
    
    def _get_n_elements_in_line(self, line, n):
        start_idx = 0
        elements = []
        for _ in range(n - 1):
            element, start_idx = self._get_next_element_in_line(line, start_idx)
            elements.append(element)

        # last element is text, so we don't need to find the end index
        elements.append(line[start_idx:-1])
        return elements



    def handle_start_query(self, query_manager, line):
        _, query_id, match_type_int, 
        pass
        
    def _handle_command(self, query_manager, line):
        command_type = command[line[0]]

        match command_type:
            case CommandType.START_QUERY:
                self.handle_start_query(query_manager, line)
            case CommandType.MATCH_DOCUMENT:
                self.handle_match_document(query_manager, line)
            case CommandType.END_QUERY:
                self.handle_end_query(query_manager, line)
            case CommandType.GET_NEXT_RES:
                self.handle_get_next_res(query_manager, line)


    def test_exact_matches(self):
        print("Start Test ...\n")

        query_manager = QueryManager()
        query_manager.start_query(query_id=1, query_text="data integration", match_type="exact", match_distance=0)
        query_manager.end_query(query_id=1)

        with open(self.small_test_fp, "r") as f:
            for line in f:
                self._handle_command(query_manager, line)

            


if __name__ == '__main__':
    unittest.main()