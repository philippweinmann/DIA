import time
from core import initialize_index, start_query, end_query, match_document, get_next_avail_res, destroy_index, ErrorCode

from datetime import timedelta
from testing_utils import timeit
import logging
logging.basicConfig()

MAX_DOC_LENGTH = 1000

def verify_retrieve_result(expected_doc_id, expected_num_res, expected_query_ids):
    err, doc_id, num_res, query_ids = get_next_avail_res()

    logging.debug(f"Retrieve Result: Doc ID={doc_id}, Num Res={num_res}, Query IDs={query_ids}")
    logging.debug(f"Expected: Doc ID={expected_doc_id}, Num Res={expected_num_res}, Query IDs={expected_query_ids}")

    assert err == ErrorCode.EC_SUCCESS, f"Error in GetNextAvailRes: {err}"
    assert doc_id == expected_doc_id
    assert num_res == expected_num_res
    assert query_ids == expected_query_ids

@timeit
def run_test(test_fp): 
    logging.info("Starting Test...")
    
    initialize_index()

    logging.info(f"Reading test file: {test_fp}")
    with open(test_fp, "r") as test_file:
        for line_num, line in enumerate(test_file):
            line = line.strip()

            # skip empty lines
            if not line:
                continue
            
            logging.debug(f"Processing line {line_num + 1}: {line[:4]}")

            line_tokens = line.split()

            ch = line_tokens[0] # command character
            id = int(line_tokens[1]) # either query_id or doc_id

            match ch:
                case 's': # s:start_query <query_id> <match_type> <match_dist> <num_keywords> list<keywords>
                    match_type = int(line_tokens[2])
                    match_dist = int(line_tokens[3])
                    keywords = " ".join(line_tokens[5:])
                    
                    logging.debug(f"StartQuery: ID={id}, Match Type={match_type}, Match Dist={match_dist}, Keywords={keywords}")
                    
                    err = start_query(id, keywords, match_type, match_dist)

                    assert err == ErrorCode.EC_SUCCESS, f"Error in StartQuery: {err}"
                
                case 'e': # e:end_query <query_id>
                    logging.debug(f"EndQuery: ID={id}")
                    err = end_query(id)
                    assert err == ErrorCode.EC_SUCCESS, f"Error in EndQuery: {err}"
                
                case 'm': # m:match_document <doc_id> <content>
                    document_content = " ".join(line_tokens[3:])
                    logging.debug(f"MatchDocument: ID={id}, Content: {document_content[:50]}")
                    err = match_document(id, document_content)
                    assert err == ErrorCode.EC_SUCCESS, f"Error in MatchDocument: {err}"
                
                case 'r': # r:retrieve <doc_id> <num_res> list<query_ids>
                    expected_num_res = int(line_tokens[2])
                    query_ids = [int(qid) for qid in line_tokens[3:]]

                    logging.debug(f"Retrieving results for document ID {id}...")
                    logging.debug(f"Expected: Num Res={expected_num_res}, Query IDs={query_ids}")

                    # Verify the results immediately
                    verify_retrieve_result(id, expected_num_res, query_ids)
                
                case _:
                    raise Exception(f"Corrupted Test File. Unknown Command '{ch}'.")

    destroy_index()
    logging.info(f"Your program has successfully passed all tests in file {file_path}.")

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO) # Change to logging.DEBUG for more detailed

    # file_path = "./data/small_test.txt"
    file_path = "./data/super_small_test.txt"
    run_test(file_path)
