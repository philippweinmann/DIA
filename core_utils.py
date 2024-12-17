from enum import Enum

class MatchType(Enum):
    EXACT = 0
    HAMMING = 1
    EDIT = 2

class ErrorCode(Enum):
    EC_SUCCESS = 0
    EC_FAIL = 1
    EC_NO_AVAIL_RES = 2