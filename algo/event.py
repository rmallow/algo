from algo.action import action

class event(action):
    def __init__(self, period=1, name="defaultEventName", calcFunc=None, params={}):
        super().__init__("event", period=period, name=name, calcFunc=calcFunc, params = params)

    def update(self, feed):
        cols = super().update(feed)
        return cols