import pandas as pd
from ..commonUtil import mpLogging
from ..commonGlobals import ACTION_GROUP
from ..commonUtil.keywordUnpacker import keywordUnpacker


def findCol(feed, col):
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
    if feed.data is not None and col in feed.data.columns:
        return feed.data[col]
    elif feed.calcData is not None and col in feed.calcData.columns:
        if feed.newCalcData is not None and col in feed.newCalcData.columns:
            return feed.calcData[col].append(feed.newCalcData[col])
        else:
            return feed.calcData[col]
    elif feed.newCalcData is not None and col in feed.newCalcData.columns:
        return feed.newCalcData[col]
    else:
        return None


def findNewCalcCol(feed, col):
    """
    @brief: find column but only in newCalc

    @param: col - column to find
    """
    if feed.newCalcData is not None and col in feed.newCalcData.columns:
        return feed.newCalcData[col]
    else:
        return None


def getParameter(parameters, key, default):
    if parameters is not None:
        return parameters.get(key, default)
    return None


ACTION_KEYWORDS_DICT = {'period': 1, 'name': 'defaultActionName', 'parameters': {},
                        'inputCols': []}

ACTION_REQUIRED_LIST = ['actionType', 'calcFunc']


class action(keywordUnpacker):
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unpack(kwargs, ACTION_KEYWORDS_DICT, required=ACTION_REQUIRED_LIST, warn=False)
        self.name = self.name.lower()
        if 'period' not in self.parameters:
            self.parameters['period'] = self.period
        # convert to lower, everything lower!
        self.inputCols = [x.lower() for x in self.inputCols]
        self.dataSet = None

    def update(self, feed):
        """
        @brief: called by action pool, updates dataSet and calls calcFunc

        @param: feed    - feed that this action is acting on
        """
        self.updateDataSet(feed)
        return self.calcFunc(self.dataSet, parameters=self.parameters)

    def updateDataSet(self, feed):
        """
        @brief: called by updates, updates dataSet by finding necessary columns and adding them

        @param: feed    - feed that this action is acting on
        """
        start = -1 * self.period
        index = feed.data.index[start: len(feed.data.index)]
        self.dataSet = pd.DataFrame(index=index)
        for col in self.inputCols:
            try:
                holder = findCol(feed, col)
                self.dataSet[col] = holder
            except ValueError:
                mpLogging.errror("Error setting column for updating data set", group=ACTION_GROUP,
                                 description=f"Name of action: {self.name} and input cols: {self.inputCols}")
                print(feed.data)
