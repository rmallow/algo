import algo.action as act
import algo.feed as afd

"""
    TODO: finish implementation for processor
    meant to be used as another action that stores data/class/model to perform analysis
"""

class processor(act.action):
    def __init__(self, period=1, name="defaultProcessorName", calcFunc=None, params={}, inputCols = []):
        super().__init__("processor", period=period, name=name, calcFunc=calcFunc, params=params, inputCols=inputCols)
        self.m_storedData = None
        
    def update(self, feed):
        super().updateDataSet(feed)