import feed

class action():
    def __init__(self, actionType, period = 1, name = "defaultActionName", calcFunc = None):
        self.m_actionType = actionType
        self.m_period = period
        self.m_name = name

        #member variables not assigned at initiation
        self.m_data = None        #might not be necessary
        self.m_lastTimestamp = None
        self.m_calcFunc = calcFunc

    def update(self, feed):
        pass