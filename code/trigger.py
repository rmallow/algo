from action import action

class trigger(action):
    def __init__(self, period=1, name = "defaultTriggerName", calcFunc = None):
        super().__init__("trigger", period=period, name=name, calcFunc=calcFunc)

        self.m_messageRouter = None

    def update(self, feed):
        super().update(feed)
        if self.m_calcFunc is not None:
            messages = self.m_calcFunc(feed)
            self.m_messageRouter.broadcast(messages)