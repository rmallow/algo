import pandas as pd
import logging

def findCol(feed, col):
    """
    finds the specified col from feed
    if col in data, return that, won't be in calc or new calc
    if col in calc check if it's also in new calc:
        return combined if also in new clac
        else return just calc col
    if col in new calc return that
    else return none
    """
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

def findNewCalcCol(feed, col):
    """
    find only in new Calc data
    """
    if feed.m_newCalcData is not None and col in feed.m_newCalcData.columns:
        return feed.m_newCalcData[col]
    else:
        return None

def getParameter(parameters, key, default):
    if parameters is not None:
        return parameters.get(key, default)

#period refers to number of units, not time
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

    def update(self, feed):
        self.updateDataSet(feed)
        return self.m_calcFunc(self.m_dataSet, parameters=self.m_parameters)
        
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

    def getCalcFunc(self):
        return self.m_calcFunc
        