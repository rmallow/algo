from .constants import DataTypeEnum
from .constants import OUTSIDE_CONSTRAINT

from .util import pandasUtil as pu

from ..commonUtil.keywordUnpacker import keywordUnpacker

import abc
import logging

"""
Base class for data importers, holds member variables that all should use and other shared functions
"""

DATA_BASE_KEYWORDS_LIST = {'key': None, 'dataType': None, 'indexName': None, 'period': None, 'columnFilter': None,
                           'upperConstraint': None, 'lowerConstraint': None, 'dayFirst': None,
                           'ordering': None}


class dataBase(keywordUnpacker, abc.ABC):
    def __init__(self, *args, **kwargs):
        self.unpack(kwargs, DATA_BASE_KEYWORDS_LIST, warn=True)

        # Convert data type to enum
        if self.dataType is not None:
            try:
                self.dataType = DataTypeEnum[self.dataType]
            except ValueError:
                logging.warning("Failed setting data type")
                logging.warning(self.dataType)

        self.end = False
        self.newCycle = False

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
            # remove columns still to be added
            dataFrame = pu.filterColumns(dataFrame, columnFilter=self.columnFilter)

            if self.hasConstraints():
                dataFrame = dataFrame.between_time(self.lowerConstraint, self.upperConstraint)

            if dataFrame.index[0] > dataFrame.index[1]:
                dataFrame = dataFrame[::-1]
            # dataFrame.index = dataFrame.index.tz_localize('UTC').tz_convert('US/Central')
        return dataFrame

    def hasConstraints(self):
        return self.lowerConstraint is not None and self.upperConstraint is not None

    def checkConstraint(self, data):
        """
        @breif: checks data index based on upper lower constraints

        @param: data - pandas dataframe with index that can be compared to constraints

        @return: if outside of constraint it will return constants.OUTSIDE_CONSTRAINT otherwise return None
        """
        # if data is not pandas or comparison to index doesn't work this will except
        # as this could be called every get Data wan't to log the except
        try:
            if data.index[0] < self.lowerConstraint or \
               data.index[-1] > self.upperConstraint:
                return OUTSIDE_CONSTRAINT
            else:
                return None
        except Exception:
            logging.warning("Exception in check constraint, check constraints were set correctly")
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
