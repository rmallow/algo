from .dataBase import dataBase
from .constants import DataTypeEnum

from .util import requestUtil as ru

import time


class dataStream(dataBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.time = None

        self.loadData()

    def getData(self, timestamp, period):
        if self.time:
            # this just feels dangerous
            while self.time < time.time() - self.period:
                pass

        returnVal = None
        if self.dataType == DataTypeEnum.REAL_TIME_REQUEST:
            returnVal = self.getDataReal(timestamp, period)

        if returnVal is not None:
            returnVal = self.dataFrameModifications(returnVal)

        self.time = time.time()
        return returnVal

    def getDataReal(self, timestamp, period):
        return ru.getPandasFromUrl(self.key)

    def loadData(self):
        return
