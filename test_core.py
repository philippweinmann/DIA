import time
import sys
from core import (
    initialize_index,
    destroy_index,
    start_query,
    end_query,
    match_document,
    get_next_avail_res,
    ErrorCode
)

# Function to get the current time in milliseconds
def GetClockTimeInMilliSec():
    return int(round(time.time() * 1000))

# Function to print time in hours, minutes, seconds, and milliseconds format
def PrintTime(milli_sec):
    v = milli_sec
    hours = v // (1000 * 60 * 60)
    v %= (1000 * 60 * 60)
    minutes = v // (1000 * 60)
    v %= (1000 * 60)
    seconds = v // 1000
    milli_seconds = v % 1000
    time_parts = []
    if hours:
        time_parts.append(f"{hours}h")
    if minutes:
        time_parts.append(f"{minutes}m")
    if seconds:
        time_parts.append(f"{seconds}s")
    if milli_seconds:
        time_parts.append(f"{milli_seconds}ms")
    formatted_time = ":".join(time_parts)
    print(f"{milli_sec}[{formatted_time}]")

# Function to run the test
def TestSigmod(test_file_str):
    print("Start Test ...")
    try:
        with open(test_file_str, "rt") as test_file:
            v = GetClockTimeInMilliSec()
            initialize_index()

            first_result = 0
            num_cur_results = 0
            max_results = 100

            cur_results_ret = [False] * max_results
            cur_results_size = [0] * max_results
            cur_results = [None] * max_results

            while True:
                line = test_file.readline()
                if not line:
                    break
                parts = line.strip().split(maxsplit=2)
                if len(parts) < 2:
                    print("Corrupted Test File.")
                    return

                ch, id_str = parts[:2]
                id = int(id_str)

                if num_cur_results and ch in ('s', 'e'):
                    for i in range(num_cur_results):

                        err, doc_id, num_res, query_ids = get_next_avail_res()


                        if err == ErrorCode.EC_NO_AVAIL_RES:
                            print("The call to GetNextAvailRes() returned EC_NO_AVAIL_RES, but there are still undelivered documents.")
                            return
                        elif err == ErrorCode.EC_FAIL:
                            print("The call to GetNextAvailRes() returned EC_FAIL.")
                            return
                        elif err != ErrorCode.EC_SUCCESS:
                            print("The call to GetNextAvailRes() returned unknown error code.")
                            return

                        if doc_id < first_result or doc_id - first_result >= num_cur_results:
                            print(f"The call to GetNextAvailRes() returned unknown document ID {doc_id}.")
                            return
                        if cur_results_ret[doc_id - first_result]:
                            print(f"The call to GetNextAvailRes() returned document (ID={doc_id}) that has been delivered before.")
                            return

                        flag_error = False
                        if num_res != cur_results_size[doc_id - first_result]:
                            flag_error = True

                        for j in range(int(num_res)):
                            if query_ids[j] != cur_results[doc_id - first_result][j]:
                                flag_error = True

                        if flag_error:
                            print(f"The call to GetNextAvailRes() returned incorrect result for document ID {doc_id}.")
                            print(f"Your answer is: {' '.join(map(str, query_ids))}")
                            print(f"The correct answer is: {' '.join(map(str, cur_results[doc_id - first_result]))}")
                            return

                        cur_results_ret[doc_id - first_result] = True
                        if num_res and query_ids:
                            query_ids.clear()

                    num_cur_results = 0

                if ch == 's':
                    match_type, match_dist, temp = int(parts[2].split()[0]), int(parts[2].split()[1]), parts[2].split(maxsplit=2)[2]
                    err = start_query(id, temp, match_type, match_dist)
                    if err == ErrorCode.EC_FAIL:
                        print("The call to StartQuery() returned EC_FAIL.")
                        return
                    elif err != ErrorCode.EC_SUCCESS:
                        print("The call to StartQuery() returned unknown error code.")
                        return

                elif ch == 'e':
                    err = end_query(id)
                    if err == ErrorCode.EC_FAIL:
                        print("The call to EndQuery() returned EC_FAIL.")
                        return
                    elif err != ErrorCode.EC_SUCCESS:
                        print("The call to EndQuery() returned unknown error code.")
                        return

                elif ch == 'm':
                    temp = parts[2]
                    err = match_document(id, temp)
                    if err == ErrorCode.EC_FAIL:
                        print("The call to MatchDocument() returned EC_FAIL.")
                        return
                    elif err != ErrorCode.EC_SUCCESS:
                        print("The call to MatchDocument() returned unknown error code.")
                        return

                elif ch == 'r':
                    try:
                        
                        num_res_str, *query_id_strs = parts[2].split()
                        num_res = int(num_res_str)
                    except ValueError:
                        print("Corrupted Test File.")
                        print(parts)  # For debugging
                        return

                    
                    if num_cur_results == 0:
                        first_result = id

                    
                    cur_results_ret[num_cur_results] = False
                    cur_results_size[num_cur_results] = num_res
                    

                    
                    query_ids = list(map(int, query_id_strs))

                    
                    while len(query_ids) < num_res:
                        query_ids.extend(map(int, test_file.readline().strip().split()))

                    
                    cur_results[num_cur_results] = query_ids[:num_res]

                    
                    num_cur_results += 1
                    print(f"Parts: {parts}") #Debugging







                else:
                    print("Corrupted Test File. Unknown Command.")
                    return

            v = GetClockTimeInMilliSec() - v
            destroy_index()
            print("Your program has successfully passed all tests.")
            print("Time=", end="")
            PrintTime(v)

    except FileNotFoundError:
        print(f"Cannot Open File {test_file_str}")

# Entry point for the test
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        TestSigmod("./data/small_test.txt")
    else:
        TestSigmod(sys.argv[1])
