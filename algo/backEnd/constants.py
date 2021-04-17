from .util.algoEnum import algoEnum

"""
----------------------------
DATA GETTER CLASS CONSTATNTS
----------------------------
"""


class DataTypeEnum(algoEnum):
    HISTORICAL_REQUEST = 1
    REAL_TIME_REQUEST = 2
    CSV = 3
    DIR = 4
    URL = 5


class DataSourceReturnEnum(algoEnum):
    NO_DATA = 0
    OUTSIDE_CONSTRAINT = 1


"""
----------------------------
FEED CONSTANTS
----------------------------
"""

INSUF_DATA = 'insufData'
COL_NF = 'colNF'
