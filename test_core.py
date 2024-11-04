import time
from core import initialize_index, start_query, end_query, match_document, get_next_avail_res, destroy_index, ErrorCode

MAX_DOC_LENGTH = 1000

def get_clock_time_in_millisec():
    return int(time.time() * 1000)

def print_time(milli_sec):
    hours = milli_sec // (1000 * 60 * 60)
    minutes = (milli_sec % (1000 * 60 * 60)) // (1000 * 60)
    seconds = (milli_sec % (1000 * 60)) // 1000
    milli_seconds = milli_sec % 1000
    print(f"{milli_sec}[{hours}h:{minutes}m:{seconds}s:{milli_seconds}ms]")

def process_retrieve_result(expected_doc_id, expected_num_res, expected_query_ids):
    doc_id, num_res, query_ids = 0, 0, []
    err, doc_id, num_res, query_ids = get_next_avail_res()


    print(f"Retrieve Result: Doc ID={doc_id}, Num Res={num_res}, Query IDs={query_ids}")
    print(f"Expected: Doc ID={expected_doc_id}, Num Res={expected_num_res}, Query IDs={expected_query_ids}")

    if err == ErrorCode.EC_NO_AVAIL_RES:
        raise Exception("Expected available results, but got EC_NO_AVAIL_RES.")

    if err != ErrorCode.EC_SUCCESS:
        raise Exception(f"Error occurred in GetNextAvailRes: {err}")

    if doc_id != expected_doc_id or num_res != expected_num_res or query_ids != expected_query_ids:
        raise Exception(f"Expected doc ID {expected_doc_id} with {expected_num_res} results, but got doc ID {doc_id} with {num_res} results.")

def run_test():
    test_file_str = "small_test.txt"  # Path to your test file
    print("Start Test...")
    
    initialize_index()

    with open(test_file_str, "r") as test_file:
        first_result = 0
        num_cur_results = 0

        cur_results_ret = [False] * 100
        cur_results_size = [0] * 100
        cur_results = [[] for _ in range(100)]

        for line_num, line in enumerate(test_file, 1):
            line = line.strip()
            if not line:
                continue
            print(f"Processing line {line_num}: {line[:4]}")
            parts = line.split()
            ch = parts[0]
            id = int(parts[1])

            if num_cur_results and (ch == 's' or ch == 'e'):
                for i in range(num_cur_results):
                    expected_doc_id = first_result + i
                    expected_num_res = cur_results_size[i]
                    expected_query_ids = cur_results[i]

                    print(f"Validating results for document ID {expected_doc_id}...")
                    process_retrieve_result(expected_doc_id, expected_num_res, expected_query_ids)

                cur_results_ret = [False] * 100
                cur_results_size = [0] * 100
                cur_results = [[] for _ in range(100)]
                num_cur_results = 0

            if ch == 's':
                match_type = int(parts[2])
                match_dist = int(parts[3])
                keywords = " ".join(parts[5:])
                print(f"StartQuery: ID={id}, Match Type={match_type}, Match Dist={match_dist}, Keywords={keywords}")
                err = start_query(id, keywords, match_type, match_dist)
                if err != ErrorCode.EC_SUCCESS:
                    raise Exception(f"Error in StartQuery: {err}")

            elif ch == 'e':
                print(f"EndQuery: ID={id}")
                err = end_query(id)
                if err != ErrorCode.EC_SUCCESS:
                    raise Exception(f"Error in EndQuery: {err}")

            elif ch == 'm':
                document_content = " ".join(parts[3:])
                print(f"MatchDocument: ID={id}, Content: {document_content[:50]}")
                err = match_document(id, document_content)
                if err != ErrorCode.EC_SUCCESS:
                    raise Exception(f"Error in MatchDocument: {err}")

            elif ch == 'r':
                expected_num_res = int(parts[2])
                query_ids = [int(qid) for qid in parts[3:]]
                print(f"Expected Results: Doc ID={id}, Num Results={expected_num_res}, Query IDs={query_ids}")

                if num_cur_results == 0:
                    first_result = id
                cur_results_ret[num_cur_results] = False
                cur_results_size[num_cur_results] = expected_num_res
                cur_results[num_cur_results] = query_ids
                num_cur_results += 1

            else:
                raise Exception(f"Corrupted Test File. Unknown Command '{ch}'.")

    destroy_index()
    print("Your program has successfully passed all tests.")

if __name__ == "__main__":
    run_test()
