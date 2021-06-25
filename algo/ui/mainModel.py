from .uiConstants import LOOP_INTERVAL_MSECS

from ..commonSettings import SETTINGS_FILE
from ..commonUtil import queueManager as qm

from ..backEnd import message as msg
from ..backEnd.util import configLoader

from PySide6 import QtCore

_requiredServerKeys = ['ip', 'port', 'authkey']


class mainModel(QtCore.QObject):
    updateOutputSignal = QtCore.Signal(msg.message)
    updateLoggingSignal = QtCore.Signal(msg.message)
    updateStatusSignal = QtCore.Signal(msg.message)

    def __init__(self):
        super().__init__()
        self.uiQueue = None
        self.mainframeQueue = None
        self.clientSeverManager = None

        settingsDict = configLoader.getKeyValueIni(SETTINGS_FILE)
        serverDict = None
        if "server" in settingsDict:
            serverDict = configLoader.getKeyValueIni(settingsDict["server"])

        if serverDict is None or not all(key in serverDict for key in _requiredServerKeys):
            serverDict = {"ip": "127.0.0.1", "port": 50000, "authkey": b"abc"}

        address = (serverDict['ip'], int(serverDict['port']))
        authkey = str.encode(serverDict['authkey'])
        self.clientSeverManager = qm.QueueManager(address=address, authkey=authkey)
        self.mainframeQueue = self.clientSeverManager.getMainframeQueue()
        self.uiQueue = self.clientSeverManager.getUiQueue()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.checkQueue)
        self.timer.start(LOOP_INTERVAL_MSECS)

    @QtCore.Slot()
    def messageMainframe(self, message):
        if self.mainframeQueue:
            self.mainframeQueue.put(message)

    @QtCore.Slot()
    def checkQueue(self):
        if self.uiQueue:
            while not self.uiQueue.empty():
                m: msg.message = self.uiQueue.get()
                if m.isUIUpdate() and m.content is not None:
                    if m.content == msg.UiUpdateType.BLOCK or m.content == msg.UiUpdateType.HANDLER:
                        self.updateOutputSignal.emit(m)
                    elif m.content == msg.UiUpdateType.LOGGING:
                        self.updateLoggingSignal.emit(m)
                    elif m.content == msg.UiUpdateType.STATUS:
                        self.updateStatusSignal.emit(m)
