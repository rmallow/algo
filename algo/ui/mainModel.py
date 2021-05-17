from .uiConstants import LOOP_INTERVAL_MSECS

from PySide6 import QtCore


class mainModel(QtCore.QObject):
    def __init__(self, mainframe):
        super().__init__()
        self.uiQueue = mainframe.uiQueue
        self.mainframeQueue = mainframe.mainframeQueue

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.checkQueue)
        self.timer.start(LOOP_INTERVAL_MSECS)

    @QtCore.Slot()
    def messageMainframe(self, message):
        self.mainframeQueue.put(message)

    @QtCore.Slot()
    def checkQueue(self):
        while not self.uiQueue.empty():
            m = self.uiQueue.get()
            if m.isUIUpdate():
                print(m.content)
