from action import action

class trigger(action):
    def __init__(self, period=1, name = "defaultTriggerName", calcFunc = None):
        super().__init__("trigger", period=period, name=name, calcFunc=calcFunc)

        self.m_messageRouter = None

    def update(self, feed):
        messages = super().update(feed)
        self.m_messageRouter.broadcast(messages)