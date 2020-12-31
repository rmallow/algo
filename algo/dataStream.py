from .dataBase import dataBase
from .constants import DataTypeEnum

from .util import requestUtil as ru

import logging
import time

class dataStream(dataBase):
    def __init__(self, key, dataType, indexName = None, period = None, columnFilter = None, upperConstraint = None, lowerConstraint = None):
        super().__init__(key, dataType, indexName, period, columnFilter, upperConstraint, lowerConstraint)
        
        self.m_time = None

    def getData(self, timestamp, period):
        if self.m_time:
            #this just feels dangerous
            while self.m_time < time.time() - self.m_period:
                pass

        returnVal = None
        if self.m_dataType == DataTypeEnum.HISTORICAL_REQUEST:
            pass
        elif self.m_dataType == DataTypeEnum.REAL_TIME_REQUEST:
            returnVal = self.getDataReal(timestamp, period)

        self.m_time = time.time()
        return returnVal

    def getDataReal(self, timestamp, period):
        return ru.getPandasFromUrl(self.m_key, indexName = self.m_indexName, columnFilter=self.m_columnFilter)

    def getDataFeed(self, timestamp, period):
        return self.getData(timestamp, period)

    def loadData(self):
        return