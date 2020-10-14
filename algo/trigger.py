import algo.feed as afd
from algo.action import action

class trigger(action):
    def __init__(self, period=1, name = "defaultTriggerName", calcFunc = None, params = {}, inputCols = []):
        super().__init__("trigger", period=period, name=name, calcFunc=calcFunc, params = params, inputCols=inputCols)

    def update(self, feed):
        super().updateDataSet(feed)
        for inputCol in self.m_inputCols:
            if afd.INSUF_DATA in self.m_dataSet[inputCol].values:
                return None
        messages = self.m_calcFunc(self.m_dataSet, parameters=self.m_parameters)
        return messages
