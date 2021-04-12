from .dataBase import dataBase
from .constants import DataTypeEnum
from .constants import OUTSIDE_CONSTRAINT

from .util import csvDataUtil as cdu
from .util import requestUtil as ru

# use this to load data and send to feeds for backtesting/simulation


class dataSim(dataBase):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.data = None
        self.lastIndex = None

        self.newCyle = False
        self.end = False

        self.loadData()

    def loadData(self):
        if self.dataType == DataTypeEnum.CSV:
            keyData = cdu.loadSingleCSV(self.key, index=self.indexName, dayFirst=self.dayFirst)
            self.key = keyData[0]
            self.data = keyData[1]
        elif self.dataType == DataTypeEnum.DIR:
            keyData = cdu.combineDirCSV(self.key, index="Local time")
            self.key = keyData[0]
            self.data = keyData[1]
        elif self.dataType == DataTypeEnum.URL:
            self.data = ru.getPandasFromUrl(self.key)

        self.data = self.dataFrameModifications(self.data)

    def getData(self, period):
        afterData = None
        if self.lastIndex is None:
            self.lastIndex = self.data.index[0]
        elif self.lastIndex == self.data.tail(1).index:
            return None
        else:
            # if just sent a new cycle message then reset new cycle var
            if self.newCycle:
                self.newCycle = False
            elif self.hasConstraints():
                # if constraints are set check to make sure were in current cycle, if not send reset OUTSIDE_CONSTRAINT
                # if eventually do something other than times, this will need to be changed
                if self.lastIndex.day != self.data.loc[self.lastIndex:].index[1].day:
                    self.newCycle = True
                    return OUTSIDE_CONSTRAINT

            # if made it here, set lastIndex to next index
            self.lastIndex = self.data.loc[self.lastIndex:].index[1]

        afterData = self.data.loc[self.lastIndex:]
        timesAfter = afterData.index
        index = -1
        for idx, time in enumerate(timesAfter):
            index = idx
            if (time - self.lastIndex).total_seconds() >= period:
                break

        if index == -1:
            # no new values to return
            return None
        elif index == 0:
            return self.data.loc[self.lastIndex:]
        else:
            return afterData[:index]
