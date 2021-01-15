import pandas as pd
import logging

"""
@brief: finds the specified col from feed
    if col in data, return that, won't be in calc or new calc
    if col in calc check if it's also in new calc:
        return combined if also in new clac
        else return just calc col
    if col in new calc return that
    else return none

@param: col - column to find throughout feed
"""
def findCol(feed, col):
    if feed.m_data is not None and col in feed.m_data.columns:
        return feed.m_data[col]
    elif feed.m_calcData is not None and col in feed.m_calcData.columns:
        if feed.m_newCalcData is not None and col in feed.m_newCalcData.columns:
            return feed.m_calcData[col].append(feed.m_newCalcData[col])
        else:
            return feed.m_calcData[col]
    elif feed.m_newCalcData is not None and col in feed.m_newCalcData.columns:
        return feed.m_newCalcData[col]
    else:
        return None

"""
@brief: find column but only in newCalc

@param: col - column to find
"""
def findNewCalcCol(feed, col):

    if feed.m_newCalcData is not None and col in feed.m_newCalcData.columns:
        return feed.m_newCalcData[col]
    else:
        return None

def getParameter(parameters, key, default):
    if parameters is not None:
        return parameters.get(key, default)

"""
@brief: base class for actions used by action pool
    - update is called in action pool which then calcualtes the apropriate dataSet
    - the dataSet is then passed into the calcFunc with the apropriate parameters

__init__:
@param: actionType  - refers to the action type that the inheriting class is, such as event/trigger
@param: period      - refers to number of units, not time
@param: name        - name of action
@param: calcFunc    - passed in function that will be called on the dataSet
@param: params      - extra parameters that are passed in each time to the calcFunc
@param: inputCols   - the columns that are used by the action and put into the dataSet
"""
class action():
    def __init__(self, actionType, period = 1, name = "defaultActionName", calcFunc = None, params = None, inputCols = []):
        self.m_actionType = actionType
        self.m_period = period
        self.m_name = name.lower()
        self.m_calcFunc = calcFunc
        self.m_parameters = {**params, 'period': period}
        self.m_inputCols = inputCols
        #convert to lower, everything LOWER!
        self.m_inputCols = [x.lower() for x in self.m_inputCols]
        self.m_dataSet = None

    """
    @brief: called by action pool, updates dataSet and calls calcFunc

    @param: feed    - feed that this action is acting on
    """
    def update(self, feed):
        self.updateDataSet(feed)
        return self.m_calcFunc(self.m_dataSet, parameters=self.m_parameters)

    """
    @brief: called by updates, updates dataSet by finding necessary columns and adding them

    @param: feed    - feed that this action is acting on
    """  
    def updateDataSet(self, feed):
        start = -1 * self.m_period
        index = feed.m_data.index[start: len(feed.m_data.index)]
        self.m_dataSet = pd.DataFrame(index=index)
        for col in self.m_inputCols:
            try:
                self.m_dataSet[col] = findCol(feed, col)
            except ValueError as e:
                logging.warning(e)
                logging.warning(col + str(index))
        