from .dataBase import dataBase

import time

DATA_FUNC_KEYWORDS_LIST = {'getFunc': None, 'setupFunc': None, 'parameters': {}}


class dataFunc(dataBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.unpack(kwargs, DATA_FUNC_KEYWORDS_LIST, warn=True)

        self.time = None

        self.loadData()

    def getData(self, period):
        if self.time:
            diff = time.time() - self.time
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
