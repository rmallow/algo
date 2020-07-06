import algo.message as msg

def testFunc(feed, **kwargs):
    return [msg.message(msg.TRIGGER_TYPE, feed.m_newData['Close'][0], name="TestMessage")]