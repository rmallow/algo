from .uiConstants import LOOP_INTERVAL_MSECS

from ..commonGlobals import RECEIVE_TIME, MAINFRAME
from ..commonSettings import SETTINGS_FILE
from ..commonUtil import queueManager as qm
from ..commonUtil.helpers import getStrTime

from ..backEnd import message as msg
from ..backEnd import messageKey
from ..backEnd.util import configLoader
from ..backEnd.util.commandProcessor import commandProcessor

import time

from PySide6 import QtCore

OUTPUT = "Output"
LOGGING = "Logging"
STATUS = "Status"
STARTUP = "Startup"


class mainModel(commandProcessor, QtCore.QObject):
    updateOutputSignal = QtCore.Signal(msg.message)
    updateLoggingSignal = QtCore.Signal(msg.message)
    updateStatusSignal = QtCore.Signal(msg.message)
    startupSignal = QtCore.Signal(msg.message)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.uiQueue = None
        self.mainframeQueue = None
        self.clientSeverManager = None
        self.incomingMessageCount = {}

        # Get server settings, if none then assume local
        settingsDict = configLoader.getKeyValueIni(SETTINGS_FILE)
        serverDict = None
        if "server" in settingsDict:
            serverDict = configLoader.getKeyValueIni(settingsDict["server"])

        port = None
        authkey = None
        ip = None
        if 'port' in serverDict:
            port = int(serverDict['port'])
        else:
            port = 50000

        if 'authkey' in serverDict:
            authkey = str.encode(serverDict['authkey'])
        else:
            authkey = b'abc'

        if 'ip' in serverDict:
            ip = serverDict['ip']
        else:
            ip = "127.0.0.1"

        # Connect to clientServerManager
        address = (ip, port)
        self.clientSeverManager = qm.QueueManager(address=address, authkey=authkey)
        self.clientSeverManager.connect()

        # Get the necessary queues from the manager
        self.mainframeQueue = self.clientSeverManager.getMainframeQueue()
        self.uiQueue = self.clientSeverManager.getUiQueue()

        # Send a startup command to the mainframe queue
        m = msg.message(msg.MessageType.COMMAND, msg.CommandType.UI_STARTUP)
        self.messageMainframe(m)

        # ui update messages to qt signals
        self.addCmdFunc(msg.UiUpdateType.BLOCK, lambda obj, _, details=None:
                        obj.emitSignalAndTrack(details, obj.updateOutputSignal))
        self.addCmdFunc(msg.UiUpdateType.HANDLER, lambda obj, _, details=None:
                        obj.emitSignalAndTrack(details, obj.updateOutputSignal))
        self.addCmdFunc(msg.UiUpdateType.LOGGING, lambda obj, _, details=None:
                        obj.emitSignalAndTrack(details, obj.updateLoggingSignal))
        self.addCmdFunc(msg.UiUpdateType.STATUS, lambda obj, _, details=None:
                        obj.emitSignalAndTrack(details, obj.updateStatusSignal))
        self.addCmdFunc(msg.UiUpdateType.STARTUP, lambda obj, _, details=None:
                        obj.emitSignalAndTrack(details, obj.startupSignal))

        # command processor functions
        self.addCmdFunc(msg.CommandType.CHECK_UI_STATUS, self.checkStatus)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.checkQueue)
        self.timer.start(LOOP_INTERVAL_MSECS)

    @QtCore.Slot()
    def messageMainframe(self, message):
        if self.mainframeQueue:
            self.mainframeQueue.put(message)

    @QtCore.Slot()
    def checkQueue(self):
        while self.uiQueue and not self.uiQueue.empty():
            m: msg.message = self.uiQueue.get()
            if not m.isMessageList():
                self.processCommand(m.content, details=m)
            else:
                for msgIter in m.content:
                    if msgIter.content is not None:
                        self.processCommand(msgIter.content, details=msgIter)

    @QtCore.Slot()
    def sendCmdStart(self):
        self.messageMainframe(msg.message(msg.MessageType.COMMAND, msg.CommandType.START))

    @QtCore.Slot()
    def sendCmdEnd(self):
        self.messageMainframe(msg.message(msg.MessageType.COMMAND, msg.CommandType.END))

    def trackMessage(self, message):
        if message.content not in self.incomingMessageCount:
            self.incomingMessageCount[message.content] = 1
        else:
            self.incomingMessageCount[message.content] += 1

        messageDetails = {RECEIVE_TIME: getStrTime(time.time())}
        messageDetails |= self.incomingMessageCount
        key = messageKey.messageKey(MAINFRAME, None)
        self.updateStatusSignal.emit(msg.message(msg.MessageType.UI_UPDATE, msg.UiUpdateType.STATUS,
                                     details=messageDetails, key=key))

    def checkStatus(self, _, details=None):
        self.trackMessage(details)
        self.messageMainframe(details)

    def emitSignalAndTrack(self, message, signal):
        self.trackMessage(message)
        signal.emit(message)
