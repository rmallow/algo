import pandas as pd

col = 'col'
period = 'period'

def findCol(feed, col):
    if col in feed.m_data.columns:
        return feed.m_data[col]
    elif feed.m_calcData is not None and col in feed.m_calcData.columns:
        if col in feed.m_newCalcData.columns:
            return feed.m_calcData[col].append(feed.m_newCalcData[col])
        else:
            return feed.m_calcData[col]
    else:
        return None

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
        if self.m_dataSet is None:
            start = -1 * self.m_period
            self.m_dataSet = pd.DataFrame(index=feed.m_data.index[start: len(feed.m_data.index)])
        for col in self.m_inputCols:
            self.m_dataSet[col] = findCol(feed, col)
        