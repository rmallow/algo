from .dataConstants import DataTypeEnum

from .util import requestUtil as ru

import logging
import time

class dataStream():
    def __init__(self, key, dataType, url, indexName = None, columnFilter = None, period = None):
        self.m_key = key
        try:
            self.m_dataType = DataTypeEnum[dataType]
        except ValueError:
            logging.warning("Failed setting data type")
            logging.warning(self.m_dataType)
        self.m_url = url
        self.m_indexName = indexName
        self.m_columnFilter = columnFilter
        self.m_period = period
        self.m_time = None

    def getData(self, timestamp, period):
        if self.m_time:
            while True:
                if self.m_time < time.time() - self.m_period:
                    break

        returnVal = None
        if self.m_dataType == DataTypeEnum.HISTORICAL:
            pass
        elif self.m_dataType == DataTypeEnum.REAL_TIME:
            returnVal = self.getDataReal(timestamp, period)

        self.m_time = time.time()
        return returnVal

    def getDataReal(self, timestamp, period):
        return ru.getPandasFromUrl(self.m_url, indexName = self.m_indexName, columnFilter=self.m_columnFilter)

    def getDataFeed(self, timestamp, period):
        return self.getData(timestamp, period)