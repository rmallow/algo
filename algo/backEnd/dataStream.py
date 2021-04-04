from .dataBase import dataBase
from .constants import DataTypeEnum

from .util import requestUtil as ru

import time


class dataStream(dataBase):
    def __init__(self, key, dataType, index="Local Time", period=1, columnFilter=None,
                 lowerConstraint=None, upperConstraint=None, dayFirst=False, **kwargs):
        self.m_time = None

        super().__init__(key, dataType, index, period, columnFilter, lowerConstraint, upperConstraint, dayFirst)

    def getData(self, timestamp, period):
        if self.m_time:
            # this just feels dangerous
            while self.m_time < time.time() - self.m_period:
                pass

        returnVal = None
        if self.m_dataType == DataTypeEnum.REAL_TIME_REQUEST:
            returnVal = self.getDataReal(timestamp, period)

        if returnVal is not None:
            returnVal = self.dataFrameModifications(returnVal)

        self.m_time = time.time()
        return returnVal

    def getDataReal(self, timestamp, period):
        return ru.getPandasFromUrl(self.m_key)

    def loadData(self):
        return
