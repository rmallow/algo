from .constants import DataSourceTypeEnum, DataSourceReturnEnum

from .util import pandasUtil as pu

from ..commonUtil.keywordUnpacker import keywordUnpacker
from ..commonUtil import mpLogging
from ..commonGlobals import DATA_GROUP

import abc

"""
Base class for data importers, holds member variables that all should use and other shared functions
"""

DATA_BASE_KEYWORDS_DICT = {'key': None, 'dataType': None, 'indexName': None, 'period': None, 'columnFilter': None,
                           'upperConstraint': None, 'lowerConstraint': None, 'dayFirst': None,
                           'ordering': None, 'sequential': False}


class dataBase(keywordUnpacker, abc.ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unpack(kwargs, DATA_BASE_KEYWORDS_DICT, warn=True)

        # Convert data type to enum
        if self.dataType is not None:
            try:
                self.dataType = DataSourceTypeEnum[self.dataType]
            except ValueError:
                mpLogging.warning("Failed setting data type",
                                  description=f"Data Type: {self.dataType}", group=DATA_GROUP)
        self.end = False
        self.newCycle = False
        self.indexNum = 0

    def dataFrameModifications(self, dataFrame):
        """
        @brief: Does modifications to dataFrame based on set values data base

        @param: dataframe - pandas dataframe to perform modiciations

        @return: Returns modified pandas dataframe or None
        """
        if dataFrame is not None:
            #

            # set columns to lower
            dataFrame.columns = [x.lower() for x in dataFrame.columns]
            if self.indexName:
                dataFrame = pu.setIndex(dataFrame, self.indexName)
            elif self.sequential:
                dataFrame.rename(index=lambda x: x + self.indexNum, inplace=True)
                self.indexNum += len(dataFrame.index)

            # remove columns still to be added
            dataFrame = pu.filterColumns(dataFrame, columnFilter=self.columnFilter)

            if self.hasConstraints():
                dataFrame = dataFrame.between_time(self.lowerConstraint, self.upperConstraint)

            if len(dataFrame.index) > 1 and dataFrame.index[0] > dataFrame.index[1]:
                dataFrame = dataFrame[::-1]
            # dataFrame.index = dataFrame.index.tz_localize('UTC').tz_convert('US/Central')
        return dataFrame

    def hasConstraints(self):
        return self.lowerConstraint is not None and self.upperConstraint is not None

    def checkConstraint(self, data):
        """
        @breif: checks data index based on upper lower constraints

        @param: data - pandas dataframe with index that can be compared to constraints

        @return: if outside of constraint it will return constants.DataSourceReturnEnum.OUTSIDE_CONSTRAINT
                     otherwise return None
        """
        # if data is not pandas or comparison to index doesn't work this will except
        # as this could be called every get Data wan't to log the except
        try:
            if data.index[0] < self.lowerConstraint or \
               data.index[-1] > self.upperConstraint:
                return DataSourceReturnEnum.OUTSIDE_CONSTRAINT
            else:
                return None
        except Exception:
            mpLogging.warning("Exception in check constraint, check constraints were set correctly", group=DATA_GROUP,
                              description=f"Lower constraint: {self.lowerConstraint} \
                                  Upper Constraint: {self.upperConstraint}")
            return None

    """
    @brief: abstract method that is normally passed to feeds to get data

    @param: timestamp   -   starting timestamp from which to get data
    @param: period      -   period of time to which get data
    """
    @abc.abstractmethod
    def getData(self, period):
        return

    """
    @brief: abstract method, sets up data getting object as needed, i.e. dataSim loading data into dataFrame
    """
    @abc.abstractmethod
    def loadData(self):
        return
