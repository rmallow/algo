from .constants import DataTypeEnum

import logging
"""
Base class for data importers, holds member variables that all should use and other shared functions
"""

class dataBase():
    def __init__(self, key, dataType, indexName, period, columnFilter):
        self.m_key = key
        try:
            self.m_dataType = DataTypeEnum[dataType]
        except ValueError:
            logging.warning("Failed setting data type")
            logging.warning(self.m_dataType)
        self.m_indexName = indexName
        self.m_period = period
        self.m_columnFilter = columnFilter
