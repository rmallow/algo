import algo.message as msg
import numpy as np

def testFunc(dataSet, parameters):
    return [msg.message(msg.TRIGGER_TYPE, dataSet.iloc[0,0], name="TestMessage")]

def crossover(dataSet, parameters):
    before = np.sign(dataSet.iloc[0, 0] - dataSet.iloc[0, 1])
    after = np.sign(dataSet.iloc[1, 0] - dataSet.iloc[1, 1])
    if before != after:
        return msg.message(msg.TRIGGER_TYPE, "crossoverMsg", name="crossover")
    else:
        return None