from action import action

class trigger(action):
    def __init__(self, period=1, name = "defaultTriggerName", calcFunc = None, cols = None):
        super().__init__("trigger", period=period, name=name, calcFunc=calcFunc, cols = cols)

        self.m_messageRouter = None

    def update(self, feed):
        messages = super().update(feed)
        for message in messages:
            self.m_messageRouter.recieve(messages)