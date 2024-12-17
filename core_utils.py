from enum import Enum

class MatchType(Enum):
    EXACT = 0
    HAMMING = 1
    EDIT = 2