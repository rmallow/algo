import algo.message as msg

def testFunc(dataSet, parameters):
    return [msg.message(msg.TRIGGER_TYPE, dataSet[0][0], name="TestMessage")]

def crossover(dataSet, parameters):
    print(dataSet)
    return msg.message(msg.TRIGGER_TYPE, "crossoverMsg", name="crossover")