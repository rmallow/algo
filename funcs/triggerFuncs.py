import numpy as np


def testFunc(dataSet, parameters=None):
    return "testMessage"


def crossover(dataSet, parameters):
    before = np.sign(dataSet.iloc[0, 0] - dataSet.iloc[0, 1])
    after = np.sign(dataSet.iloc[1, 0] - dataSet.iloc[1, 1])
    if before != after:
        return dataSet.index[0]
    else:
        return None


def under(dataSet, parameters=None):
    if dataSet.iloc[0, 0] < parameters['factor']:
        return True


def over(dataSet, parameters=None):
    if dataSet.iloc[0, 0] > parameters['factor']:
        return True
