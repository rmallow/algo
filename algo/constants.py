from .util.algoEnum import algoEnum

"""
DATA CONSTATNTS
"""

class DataTypeEnum(algoEnum):
    HISTORICAL_REQUEST = 1
    REAL_TIME_REQUEST = 2
    CSV = 3
    DIR = 4
    URL = 5

INSUF_DATA = 'insufData'
COL_NF = 'colNF'