from .dataBase import dataBase

import time

DATA_FUNC_KEYWORDS_LIST = {'getFunc': None, 'setupFunc': None, 'params': {}}


class dataFunc(dataBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.unpack(kwargs, DATA_FUNC_KEYWORDS_LIST, warn=True)

        self.time = None

        self.loadData()

    def getData(self, period):
        if self.time:
            # this just feels dangerous
            while self.time < time.time() - self.period:
                pass

        returnVal = self.getFunc(**self.params)

        if returnVal is not None:
            returnVal = self.dataFrameModifications(returnVal)

        self.time = time.time()
        return returnVal

    def loadData(self):
        if self.setupFunc:
            if self.params is not None and isinstance(self.params, dict):
                self.params |= self.setupFunc(**self.params)
            else:
                self.params = self.setupFunc
