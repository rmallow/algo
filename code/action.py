import feed

class action():
    def __init__(self, actionType, period = 1, name = "defaultActionName", calcFunc = None):
        self.m_actionType = actionType
        self.m_period = period
        self.m_name = name

        #member variables not assigned at initiation
        self.m_calcFunc = calcFunc

    def update(self, feed, **kwargs):
        return self.m_calcFunc(feed, period = self.m_period, kwargs=kwargs)