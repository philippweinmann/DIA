from testing_utils import timeit
import logging
logging.basicConfig()
from core_utils import ErrorCode

# since we are using the same testing code for all different implementations,
# let's add the correct class to the test driver.

@timeit
def run_test_driver(test_fp, core_class): 
    logging.info("Starting Test...")
    
    core_class.initialize_index()

    logging.info(f"Reading test file: {test_fp}")
    with open(test_fp, "r") as test_file:
        for line_num, line in enumerate(test_file):
            print(line_num, end="\r")
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
                    
                    err = core_class.start_query(id, keywords, match_type, match_dist)

                    assert err == ErrorCode.EC_SUCCESS, f"Error in StartQuery: {err}"
                
                case 'e': # e:end_query <query_id>
                    logging.debug(f"EndQuery: ID={id}")
                    err = core_class.end_query(id)
                    assert err == ErrorCode.EC_SUCCESS, f"Error in EndQuery: {err}"
                
                case 'm': # m:match_document <doc_id> <content>
                    document_content = " ".join(line_tokens[3:])
                    logging.debug(f"MatchDocument: ID={id}, Content: {document_content[:50]}")
                    err = core_class.match_document(id, document_content)
                    assert err == ErrorCode.EC_SUCCESS, f"Error in MatchDocument: {err}"
                
                case 'r': # r:retrieve <doc_id> <num_res> list<query_ids>
                    expected_num_res = int(line_tokens[2])
                    doc_id = id

                    expected_query_ids = set([int(qid) for qid in line_tokens[3:]])

                    logging.debug(f"Retrieving results for document ID {id}...")
                    logging.debug(f"Expected: Num Res={expected_num_res}, Expected Query IDs={expected_query_ids}")

                    # Verify the results immediately
                    err, predicted_doc_id, predicted_num_res, predicted_query_ids = core_class.get_next_avail_res()
                    predicted_query_ids = set(predicted_query_ids)
                    
                    logging.debug(f"Expected: Doc ID={id}, Num Res={expected_num_res}, Query IDs={expected_query_ids}")
                    assert err == ErrorCode.EC_SUCCESS, f"Error in GetNextAvailRes: {err}"
                    assert predicted_doc_id == doc_id
                    assert predicted_num_res == expected_num_res, f"Predicted Num Res: {predicted_num_res}, Expected Num Res: {expected_num_res}, Query IDs: {predicted_query_ids}, Expected Query IDs: {expected_query_ids}, line: {line_num}"
                    assert predicted_query_ids == expected_query_ids
                
                case _:
                    raise Exception(f"Corrupted Test File. Unknown Command '{ch}'.")

    core_class.destroy_index()
    logging.info(f"Your program has successfully passed all tests in file {file_path}.")

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO) # Change to logging.DEBUG for more detailed

    file_path = "./data/small_test.txt"
    # file_path = "./data/super_small_test.txt"

    # here we can choose which implementation to test
    # 1. reference implementation:
    from core import ReferenceCore
    referenceCore = ReferenceCore()

    run_test_driver(file_path, referenceCore)
