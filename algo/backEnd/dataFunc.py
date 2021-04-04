from .dataBase import dataBase

import time


class dataFunc(dataBase):
    def __init__(self, setupFunc, getFunc, dataType=None, key=None, params={}, indexName="Local Time", period=1,
                 columnFilter=None, lowerConstraint=None, upperConstraint=None, dayFirst=False):
        self.m_time = None
        self.m_getFunc = getFunc
        self.m_setupFunc = setupFunc
        self.m_params = params

        super().__init__(key, dataType, indexName, period, columnFilter, lowerConstraint, upperConstraint, dayFirst)

    def getData(self, timestamp, period):
        if self.m_time:
            # this just feels dangerous
            while self.m_time < time.time() - self.m_period:
                pass

        returnVal = self.m_getFunc(**self.m_params)

        if returnVal is not None:
            returnVal = self.dataFrameModifications(returnVal)

        self.m_time = time.time()
        return returnVal

    def loadData(self):
        self.m_params |= self.m_setupFunc(**self.m_params)
