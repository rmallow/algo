from trigger import trigger
from event import event
from block import block
from blockManager import blockManager
from dataSim import dataSim
from feed import feed
import threading
import time
import os
import sys

def main():

    actionList = []
    actionList.append(trigger(timer = 1, name = "test1"))
    actionList.append(event(None, timer = 2, name = "test2"))
    actionList.append(trigger(onFeedChange = True, name = "changeTest"))
    actionList.append(trigger(onFeedChange=True, name="changeTest2"))
    actionList.append(trigger(onFeedChange=True, name="changeTestend"))
    for num in range(0, 50):
        actionList.append(trigger(onFeedChange = True, name ="changetest"+str(num)))
    dS = dataSim(os.path.abspath(os.getcwd() + "/../../data/m1test/AAPL.USUSD_Candlestick_1_M_BID_01.04.2020-03.04.2020.csv"), 'csv')
    testFeed = feed(dS.asyncGetData)
    testBlock = block(actionList, testFeed)
    testBlock.m_feed.m_period = 1800
    testBlock.start()
    """
    time.sleep(2)
    count = 0
    while not dS.m_newDay:
        testBlock.m_feed.update()
        count += 1
        time.sleep(.5)
    testBlock.m_pool.m_scheduler.end()
    """
    print(testBlock.m_feed.m_data['Volume'].sum())
if __name__ == '__main__':
    main()