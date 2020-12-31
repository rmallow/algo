from .constants import DataTypeEnum
from .constants import OUTSIDE_CONSTRAINT

import abc
import logging

"""
Base class for data importers, holds member variables that all should use and other shared functions
"""

class dataBase(abc.ABC):
    def __init__(self, key, dataType, indexName, period, columnFilter, upperConstraint, lowerConstraint):
        self.m_key = key
        try:
            self.m_dataType = DataTypeEnum[dataType]
        except ValueError:
            logging.warning("Failed setting data type")
            logging.warning(self.m_dataType)
        self.m_indexName = indexName
        self.m_period = period
        self.m_columnFilter = columnFilter

        self.m_upperConstraint = upperConstraint
        self.m_lowerConstraint = lowerConstraint

        self.m_newCycle = False
        self.loadData()

    """
    @breif: checks data index based on upper lower constraints

    @param: data - pandas dataframe with index that can be compared to constraints

    @return: if outside of constraint it will return constants.OUTSIDE_CONSTRAINT otherwise return None
    """
    def checkConstraint(self, data):
        #if data is not pandas or comparison to index doesn't work this will except
        #as this could be called every get Data wan't to log the except
        try:
            if data.index[0] < self.m_lowerConstraint or \
                data.index[-1] > self.m_lowerConstraint:
                return OUTSIDE_CONSTRAINT
            else:
                return None
        except:
            logging.warning("Exception in check constraint, check constraints were set correctly")
            return None

    """
    @brief: abstract method that is normally passed to feeds to get data

    @param: timestamp   -   starting timestamp from which to get data
    @param: period      -   period of time to which get data
    """
    @abc.abstractmethod
    def getData(self, timestamp, period):
        return

    """
    @brief: abstract method, sets up data getting object as needed, i.e. dataSim loading data into self.m_data
    """
    @abc.abstractmethod
    def loadData(self):
        return
