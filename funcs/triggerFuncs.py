import algo.message as msg

def testFunc(dataSet, parameters):
    return [msg.message(msg.TRIGGER_TYPE, dataSet['close'][0], name="TestMessage")]