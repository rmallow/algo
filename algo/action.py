col = 'col'
period = 'period'



class action():
    def __init__(self, actionType, period = 1, name = "defaultActionName", calcFunc = None, params = None):
        self.m_actionType = actionType
        self.m_period = period
        self.m_name = name
        self.m_calcFunc = calcFunc
        self.m_parameters = {**params, 'period':period}

    def update(self, feed):
        return self.m_calcFunc(feed, self.m_parameters)