from .dataBase import dataBase
from .constants import DataTypeEnum
from .constants import OUTSIDE_CONSTRAINT

from .util import csvDataUtil as cdu
from .util import requestUtil as ru

# use this to load data and send to feeds for backtesting/simulation


class dataSim(dataBase):
    def __init__(self, key, dataType, indexName="Local Time", period=1, columnFilter=None, lowerConstraint=None,
                 upperConstraint=None, dayFirst=False):
        self.m_data = None
        self.m_lastIndex = None

        super().__init__(key, dataType, indexName, period, columnFilter, lowerConstraint, upperConstraint, dayFirst)

    def loadData(self):
        if self.m_dataType == DataTypeEnum.CSV:
            keyData = cdu.loadSingleCSV(self.m_key, index=self.m_indexName, dayFirst=self.m_dayFirst)
            self.m_key = keyData[0]
            self.m_data = keyData[1]
        elif self.m_dataType == DataTypeEnum.DIR:
            keyData = cdu.combineDirCSV(self.m_key, index="Local time")
            self.m_key = keyData[0]
            self.m_data = keyData[1]
        elif self.m_dataType == DataTypeEnum.URL:
            self.m_data = ru.getPandasFromUrl(self.m_key)

        self.m_data = self.dataFrameModifications(self.m_data)

    def getData(self, period):
        afterData = None
        if self.m_lastIndex is None:
            self.m_lastIndex = self.m_data.index[0]
        elif self.m_lastIndex == self.m_data.tail(1).index:
            return None
        else:
            # if just sent a new cycle message then reset new cycle var
            if self.m_newCycle:
                self.m_newCycle = False
            elif self.hasConstraints():
                # if constraints are set check to make sure were in current cycle, if not send reset OUTSIDE_CONSTRAINT
                # if eventually do something other than times, this will need to be changed
                if self.m_lastIndex.day != self.m_data.loc[self.m_lastIndex:].index[1].day:
                    self.m_newCycle = True
                    return OUTSIDE_CONSTRAINT

            # if made it here, set lastIndex to next index
            self.m_lastIndex = self.m_data.loc[self.m_lastIndex:].index[1]

        afterData = self.m_data.loc[self.m_lastIndex:]
        timesAfter = afterData.index
        index = -1
        for idx, time in enumerate(timesAfter):
            index = idx
            if (time - self.m_lastIndex).total_seconds() >= period:
                break

        if index == -1:
            # no new values to return
            return None
        elif index == 0:
            return self.m_data.loc[self.m_lastIndex:]
        else:
            return afterData[:index]
