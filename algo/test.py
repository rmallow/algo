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
import importlib
import message

def testCalcFunc(feed, **kwargs):
    return {"test1":123}

def testCalcFunc2(feed, **kwargs):
    testCol = feed.m_newCalcData['test1']
    array1 = []
    array2 = []
    index = 1
    for val in testCol:
        array1.append(val + index)
        array2.append(val + index * 2)
        index += 1
    
    return {"test2":array1,"test3":array2}

def testCalcFunc3(feed, **kwargs):
    open = feed.m_newData['Open']
    close = feed.m_newData['Close']
    array = []
    for p1, p2 in zip(open, close):
        array.append(p1 - p2)
        
    return {"diff": array}
    
def testRSI(feed):
    pass

def testTriggerFunc(feed, **kwargs):
    return message.message(message.TRIGGER_TYPE, "lol")
    
def main():

    actionList = []
    actionList.append(event(period=1, name="testEvent1", calcFunc=testCalcFunc))

    func = getattr(importlib.import_module("eventFuncs"), "smaFunc")
    
    actionList.append(event(period=300, name="sma", calcFunc=func))

    dS = dataSim(os.path.abspath(os.getcwd() + "/../../data/m1test/AAPL.USUSD_Candlestick_1_M_BID_01.04.2020-03.04.2020.csv"), 'csv')
    testFeed = feed(dS.asyncGetData)
    testBlock = block(actionList, testFeed, None)
    testBlock.m_feed.m_period = 60
    testBlock.start()

    print(testFeed.m_data)
    print(testFeed.m_newData)
    print(testFeed.m_calcData)
   
    print(testBlock.m_feed.m_data['Volume'].sum())

    print(message.COMMAND_TYPE)
if __name__ == '__main__':
    main()