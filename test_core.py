import time
from core import initialize_index, start_query, end_query, match_document, get_next_avail_res, destroy_index, ErrorCode

import logging
logging.basicConfig()

MAX_DOC_LENGTH = 1000

def get_clock_time_in_millisec():
    return int(time.time() * 1000)

def print_time(milli_sec):
    hours = milli_sec // (1000 * 60 * 60)
    minutes = (milli_sec % (1000 * 60 * 60)) // (1000 * 60)
    seconds = (milli_sec % (1000 * 60)) // 1000
    milli_seconds = milli_sec % 1000
    print(f"{milli_sec}[{hours}h:{minutes}m:{seconds}s:{milli_seconds}ms]")

def verify_retrieve_result(expected_doc_id, expected_num_res, expected_query_ids):
    err, doc_id, num_res, query_ids = get_next_avail_res()

    logging.debug(f"Retrieve Result: Doc ID={doc_id}, Num Res={num_res}, Query IDs={query_ids}")
    logging.debug(f"Expected: Doc ID={expected_doc_id}, Num Res={expected_num_res}, Query IDs={expected_query_ids}")

    if err == ErrorCode.EC_NO_AVAIL_RES:
        raise Exception("Expected available results, but got EC_NO_AVAIL_RES.")

    if err != ErrorCode.EC_SUCCESS:
        raise Exception(f"Error occurred in GetNextAvailRes: {err}")

    assert doc_id == expected_doc_id
    assert num_res == expected_num_res
    assert query_ids == expected_query_ids

def run_test(test_fp): 
    print("Starting Test...")

    start_time = get_clock_time_in_millisec()
    
    initialize_index()

    logging.info(f"Reading test file: {test_fp}")
    with open(test_fp, "r") as test_file:
        first_result = 0
        num_cur_results = 0

        cur_results_ret = [False] * 100
        cur_results_size = [0] * 100
        cur_results = [[] for _ in range(100)]

        for line_num, line in enumerate(test_file):
            line = line.strip()

            # skip empty lines
            if not line:
                continue
            
            logging.debug(f"Processing line {line_num + 1}: {line[:4]}")

            line_tokens = line.split()

            ch = line_tokens[0] # command character
            id = int(line_tokens[1]) # either query_id or doc_id

            if num_cur_results and (ch == 's' or ch == 'e'):
                for i in range(num_cur_results):
                    expected_doc_id = first_result + i
                    expected_num_res = cur_results_size[i]
                    expected_query_ids = cur_results[i]

                    logging.debug(f"Validating results for document ID {expected_doc_id}...")

                    verify_retrieve_result(expected_doc_id, expected_num_res, expected_query_ids)

                cur_results_ret = [False] * 100
                cur_results_size = [0] * 100
                cur_results = [[] for _ in range(100)]
                num_cur_results = 0

            if ch == 's':
                # s:start_query <query_id> <match_type> <match_dist> <num_keywords> list<keywords>

                match_type = int(line_tokens[2])
                match_dist = int(line_tokens[3])
                keywords = " ".join(line_tokens[5:])
                
                logging.debug(f"StartQuery: ID={id}, Match Type={match_type}, Match Dist={match_dist}, Keywords={keywords}")
                
                err = start_query(id, keywords, match_type, match_dist)

                assert err == ErrorCode.EC_SUCCESS, f"Error in StartQuery: {err}"

            elif ch == 'e':
                # e:end_query <query_id>

                logging.debug(f"EndQuery: ID={id}")

                err = end_query(id)

                assert err == ErrorCode.EC_SUCCESS, f"Error in EndQuery: {err}"

            elif ch == 'm':
                # m:match_document <doc_id> <content>

                document_content = " ".join(line_tokens[3:])
                
                logging.debug(f"MatchDocument: ID={id}, Content: {document_content[:50]}")
                
                err = match_document(id, document_content)
                
                assert err == ErrorCode.EC_SUCCESS, f"Error in MatchDocument: {err}"

            elif ch == 'r':
                # r:retrieve <doc_id> <num_res> list<query_ids>
                expected_num_res = int(line_tokens[2])
                query_ids = [int(qid) for qid in line_tokens[3:]]

                if num_cur_results == 0:
                    first_result = id
                cur_results_ret[num_cur_results] = False
                cur_results_size[num_cur_results] = expected_num_res
                cur_results[num_cur_results] = query_ids
                num_cur_results += 1

            else:
                raise Exception(f"Corrupted Test File. Unknown Command '{ch}'.")

    destroy_index()
    print(f"Your program has successfully passed all tests in file {file_path}.")

    end_time = get_clock_time_in_millisec()
    elapsed_time = end_time - start_time
    print("Elapsed Time: ", end="")
    print_time(elapsed_time)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG) # Change to logging.DEBUG for more detailed

    file_path = "./data/small_test.txt"
    run_test(file_path)
