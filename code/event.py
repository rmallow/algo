from action import action

class event(action):
    def __init__(self, period = 1, name = "defaultEventName", calcFunc = None):
        super().__init__("event", period=period, name=name, calcFunc=calcFunc)

    def update(self, feed):
        cols = super().update(feed)
        feed.addNewCalcCols(cols)