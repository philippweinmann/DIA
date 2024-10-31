# core.py version 1.0


import numpy as np

MAX_WORD_LENGTH = 256
MAX_DOC_LENGTH = 1000
MAX_QUERY_LENGTH = 256
oo = float('inf')

class ErrorCode:
    EC_SUCCESS = 0
    EC_FAIL = 1
    EC_NO_AVAIL_RES = 2

class MatchType:
    MT_EXACT_MATCH = 0
    MT_HAMMING_DIST = 1
    MT_EDIT_DIST = 2

class Query:
    def __init__(self, query_id, string, match_type, match_dist):
        self.query_id = query_id
        self.str = string
        self.match_type = match_type
        self.match_dist = match_dist

class Document:
    def __init__(self, doc_id, num_res, query_ids):
        self.doc_id = doc_id
        self.num_res = num_res
        self.query_ids = query_ids

queries = []
docs = []

def edit_distance(a, b):
    na, nb = len(a), len(b)
    T = np.zeros((2, nb + 1), dtype=int)
    
    for ib in range(nb + 1):
        T[0][ib] = ib

    for ia in range(1, na + 1):
        cur = ia % 2
        prev = 1 - cur
        T[cur][0] = ia

        for ib in range(1, nb + 1):
            d1 = T[prev][ib] + 1
            d2 = T[cur][ib - 1] + 1
            d3 = T[prev][ib - 1] + (0 if a[ia - 1] == b[ib - 1] else 1)
            T[cur][ib] = min(d1, d2, d3)

    return T[na % 2][nb]

def hamming_distance(a, b):
    if len(a) != len(b):
        return oo
    return sum(1 for x, y in zip(a, b) if x != y)

def initialize_index():
    global queries, docs
    queries = []
    docs = []
    return ErrorCode.EC_SUCCESS

def destroy_index():
    return ErrorCode.EC_SUCCESS

def start_query(query_id, query_str, match_type, match_dist):
    query = Query(query_id, query_str, match_type, match_dist)
    queries.append(query)
    return ErrorCode.EC_SUCCESS

def end_query(query_id):
    global queries
    queries = [q for q in queries if q.query_id != query_id]
    return ErrorCode.EC_SUCCESS

def match_document(doc_id, doc_str):
    global queries, docs
    cur_doc_str = doc_str.strip()
    query_ids = []

    for query in queries:
        matching_query = True
        for qword in query.str.split():
            matching_word = False
            for dword in cur_doc_str.split():
                if query.match_type == MatchType.MT_EXACT_MATCH and qword == dword:
                    matching_word = True
                elif query.match_type == MatchType.MT_HAMMING_DIST and hamming_distance(qword, dword) <= query.match_dist:
                    matching_word = True
                elif query.match_type == MatchType.MT_EDIT_DIST and edit_distance(qword, dword) <= query.match_dist:
                    matching_word = True

                if matching_word:
                    break

            if not matching_word:
                matching_query = False
                break

        if matching_query:
            query_ids.append(query.query_id)

    docs.append(Document(doc_id, len(query_ids), query_ids if query_ids else None))
    return ErrorCode.EC_SUCCESS

def get_next_avail_res():
    if not docs:
        return ErrorCode.EC_NO_AVAIL_RES, None, 0, []
    
    doc = docs.pop(0)
    return ErrorCode.EC_SUCCESS, doc.doc_id, doc.num_res, doc.query_ids if doc.query_ids else []

