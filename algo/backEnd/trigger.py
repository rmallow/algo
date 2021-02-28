from .action import action
from . import constants as con


class trigger(action):
    def __init__(self, period=1, name="defaultTriggerName", calcFunc=None, params={}, inputCols=[]):
        super().__init__("trigger", period=period, name=name, calcFunc=calcFunc, params=params, inputCols=inputCols)

    """
    TODO: change trigger update to better match event update:
            - iterate through data set as approriate but follow valid index convention
            - might be best to try and consolidate event functionality to action
            - as processor will also use that
    """
    def update(self, feed):
        super().updateDataSet(feed)
        for inputCol in self.m_inputCols:
            if con.INSUF_DATA in self.m_dataSet[inputCol].values:
                return None
        messages = self.m_calcFunc(self.m_dataSet, parameters=self.m_parameters)
        return messages
