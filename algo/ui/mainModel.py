from .uiConstants import LOOP_INTERVAL_MSECS

from ..backEnd import message as msg

from PySide6 import QtCore


class mainModel(QtCore.QObject):
    updateOutputSignal = QtCore.Signal(msg.message)
    updateLoggingSignal = QtCore.Signal(msg.message)
    updateStatusSignal = QtCore.Signal(msg.message)

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
            m: msg.message = self.uiQueue.get()
            if m.isUIUpdate() and m.content is not None:
                if m.content == msg.UiUpdateType.BLOCK or m.content == msg.UiUpdateType.HANDLER:
                    self.updateOutputSignal.emit(m)
                elif m.content == msg.UiUpdateType.LOGGING:
                    self.updateLoggingSignal.emit(m)
                elif m.content == msg.UiUpdateType.STATUS:
                    self.updateStatusSignal.emit(m)
