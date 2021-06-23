from .dataBase import dataBase

from ..commonUtil import mpLogging
from ..commonGlobals import DATA_GROUP

import time

DATA_FUNC_KEYWORDS_LIST = {'getFunc': None, 'setupFunc': None, 'parameters': {}}


class dataFunc(dataBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.unpack(kwargs, DATA_FUNC_KEYWORDS_LIST, warn=True)

        self.time = None

        self.loadData()

    def getData(self, period):
        mpLogging.info("Data func getting data", group=DATA_GROUP)
        if self.time:
            diff = time.time() - self.time
            if self.period - diff > 0:
                time.sleep(self.period-diff)

        returnVal = self.getFunc(**self.parameters)

        if returnVal is not None:
            returnVal = self.dataFrameModifications(returnVal)

        self.time = time.time()
        return returnVal

    def loadData(self):
        if self.setupFunc:
            if self.parameters is not None and isinstance(self.parameters, dict):
                self.parameters |= self.setupFunc(**self.parameters)
            else:
                self.parameters = self.setupFunc
