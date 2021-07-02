# Local common includes
from .commonSettings import SETTINGS_FILE
from .commonGlobals import ITEM, SEND_TIME, BACK_TIME, BLOCK, HANDLER

# Common Util includes
from .commonUtil import mpLogging
from .commonUtil.helpers import getStrTime
from .commonUtil import queueManager as qm

# Back End includes
from .backEnd import message as msg
from .backEnd import messageKey as msgKey
from .backEnd.messageRouter import messageRouter
from .backEnd.blockManager import blockManager
from .backEnd.handlerManager import handlerManager
from .backEnd.handlerData import handlerData
from .backEnd.util import configLoader
from .backEnd.util.commandProcessor import commandProcessor

# Multi/Asyncio/Threading includes
import multiprocessing as mp
# multiprocess is Dill version of multiprocessing
import multiprocessing as dillMp
# Lots of appreciation for aioprocessing:
# https://github.com/dano/aioprocessing
import aioprocessing
import threading

# python lib includes
import logging
import configparser
import time

MAINFRAME_QUEUE_CHECK_TIMER = .3
LOGGING_QUEUE_CHECK_TIMER = .5
STATUS_CHECK_TIMER = 1
UI_STATUS_CHECK_TIMER = 5
UI_SEND_STATUS_CHECK = 1


class mainframe(commandProcessor):

    def __init__(self):
        super().__init__()
        # have to set the level for logging
        logging.getLogger().setLevel(logging.INFO)

        # Set up item managers, unrelated to multiprocessing managers
        self.handlerManager = None
        self.blockManager = None
        self.sharedData = handlerData()

        # Load defaults
        self.loader = configLoader.configLoader(SETTINGS_FILE)

        # Set up multiprocessing items
        self.processDict = {}
        self.statusDict = {}
        self.routerProcess = None
        # This manager is for providing queues for the Router process
        self.AioManager = aioprocessing.AioManager()

        # This manager is for providing dill queues for the block processes
        self.dillBlockManager = dillMp.Manager()

        port = None
        authkey = None
        if "server.port" in self.loader.valueDict:
            port = int(self.loader.valueDict["server.port"])
        else:
            port = 50000
        # address is empty as the client will be acessing it
        address = ('', port)

        if "server.authkey" in self.loader.valueDict:
            authkey = str.encode(self.loader.valueDict["server.authkey"])
        else:
            authkey = b"abc"

        # This manager is for cleint sessions to acess these queues
        self.clientSeverManager = qm.QueueManager(address=address, authkey=authkey)

        print(f"Starting up server manager Address ip: {address[0]} port: {address[1]} and authkey: {authkey}")
        # This queue is complicated as it's used both by local processes, that won't going through manager to get it
        # But it will also be used by queues that are only going to be acessing it by manager
        self.mainframeQueue = mp.Queue(-1)
        qm.QueueManager.register("getMainframeQueue", callable=lambda: self.mainframeQueue)

        # This queue will only be used by mainframe and ui main model
        self.uiQueue = mp.Queue(-1)
        qm.QueueManager.register("getUiQueue", callable=lambda: self.uiQueue)

        # start up the manager thread for serving its objects
        threading.Thread(target=self.clientSeverManager.get_server().serve_forever).start()

        # we use regular multiprocessing here because otherwise the Dill queue will send to log which
        # causes an infinite loop in our mpLogging module
        # we don't need dill for this queue so it's okay to just use regular multiprocessing queue
        # this queue is only used "locally" so it won't need to be connected to the manager
        self.loggingQueue = mp.Queue(-1)

        # set up flag variables
        self.uiConnected = False
        self.pendingUiMessages = []
        self.uiLastTime = None

        # add commands for processor
        self.addCmdFunc(msg.CommandType.ADD_OUTPUT_VIEW, mainframe.addOutputView)
        self.addCmdFunc(msg.CommandType.UI_STARTUP, mainframe.sendStartupData)
        self.addCmdFunc(msg.CommandType.CHECK_UI_STATUS, mainframe.sendStatusCheck)

        # Get other config files to load
        config = configparser.ConfigParser()
        config.read(SETTINGS_FILE)
        blockConfigFile = ""
        handlerConfigFile = ""
        if 'Configs' in config:
            blockConfigFile = config.get('Configs', 'Block', fallback="")
            handlerConfigFile = config.get('Configs', 'Handler', fallback="")

        # init handler manager
        self.handlerManager = handlerManager(self.sharedData)
        self.loadHandlerConfig(handlerConfigFile)

        # init message router
        # we use an aio queue here as it needs to be compatible with asyncio
        # router and handlers use asyncio as handlers could have a lot of output operations
        # that are best suited to asyncio
        self.messageRouter = messageRouter(self.handlerManager.messageSubscriptions, self.sharedData,
                                           self.AioManager.AioQueue())

        # init block manager
        self.blockManager = blockManager(self.messageRouter)
        self.loadBlockConfig(blockConfigFile)

        for _, block in self.blockManager.blocks.items():
            block.blockQueue = self.dillBlockManager.Queue()
            block.mainframeQueue = self.mainframeQueue

        # this will set the current working directory from wherever to the directory this file is in
        # sys.path.append(os.path.dirname(os.path.abspath(sys.modules[__name__].__file__)))
        # removed this on 7/1/2021, if it doesn't have any issues after a month, permanently take out
        # dirPath = os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))
        # os.chdir(dirPath)
        mpLogging.info("Finished initializing mainframe")

    def sendToUi(self, message):
        if self.uiQueue is not None:
            if self.uiConnected:
                if len(self.pendingUiMessages) > 0:
                    self.sendPendingUiMessages()
                self.uiQueue.put(message)
            else:
                self.pendingUiMessages.append(message)
        else:
            mpLogging.error("Major error, ui queue is none, this should never happen")

    def sendPendingUiMessages(self):
        mpLogging.info("Sending pending messages to the UI")
        m = msg.message(msg.MessageType.MESSAGE_LIST, self.pendingUiMessages)
        self.uiQueue.put(m)
        self.pendingUiMessages = []

    def checkMainframeQueue(self):
        while not self.mainframeQueue.empty():
            message = self.mainframeQueue.get()
            if isinstance(message, msg.message):
                if message.isCommand():
                    self.processCommand(message.content, message.details)
                elif message.isUIUpdate():
                    if message.content == msg.UiUpdateType.STATUS:
                        # Extra handling for status, adding back time and removing from status dict
                        # we want to do this, removing from the dict, even if uiQueue is not present
                        code = message.key.sourceCode
                        if code in self.statusDict:
                            del self.statusDict[code]
                            message.details[BACK_TIME] = getStrTime(time.time())
                        else:
                            mpLogging.error("Trying to remove code from status dict that isn't present",
                                            description=f"Code: {code}")
                            continue
                    self.sendToUi(message)
        # schedule it again after the timer
        threading.Timer(MAINFRAME_QUEUE_CHECK_TIMER, self.checkMainframeQueue).start()

    def checkLoggingQueue(self):
        # Check whta's in the logging queue, if the ui queue exists send to that
        while not self.loggingQueue.empty():
            recordData = self.loggingQueue.get()
            if recordData:
                uiLoggingMessage = msg.message(msg.MessageType.UI_UPDATE, content=msg.UiUpdateType.LOGGING,
                                               details=recordData)
                self.sendToUi(uiLoggingMessage)
        # schedule it again after the timer
        threading.Timer(LOGGING_QUEUE_CHECK_TIMER, self.checkLoggingQueue).start()

    def sendStatusCheck(self, content, details=None):
        self.uiLastTime = time.time()
        if not self.uiConnected:
            # So we got a status message back after we thought the ui was disconnected, so start it back up again
            self.sendStartupData()
        # we'll just reply by sending the message back in 10 seconds
        threading.Timer(UI_SEND_STATUS_CHECK, self.sendToUi,
                        [msg.message(msg.MessageType.COMMAND, content=msg.CommandType.CHECK_UI_STATUS)])

    def checkItemStatus(self):
        # Check the status of the current running blocks
        for code, block in self.blockManager.blocks.items():
            if code not in self.statusDict:
                sendTimeFloat = time.time()
                block.blockQueue.put(msg.message(msg.MessageType.COMMAND, content=msg.CommandType.CHECK_STATUS,
                                     details={SEND_TIME: getStrTime(sendTimeFloat)}))
                self.statusDict[code] = sendTimeFloat
            else:
                if time.time() - self.statusDict[code] > 60:
                    # block has not responded for more than 60 seconds to we're assuming it's not responsive
                    # so we'll remove it from the status dict so it's checked again
                    m = msg.message(msg.MessageType.UI_UPDATE, content=msg.UiUpdateType.STATUS,
                                    details={SEND_TIME: self.statusDict[code]}, key=msgKey.messageKey(code, None))
                    self.sendToUi(m)
                    del self.statusDict[code]
        # schedule it again after the timer
        threading.Timer(STATUS_CHECK_TIMER, self.checkItemStatus).start()

    def init(self):
        threading.Timer(MAINFRAME_QUEUE_CHECK_TIMER, self.checkMainframeQueue).start()
        threading.Timer(LOGGING_QUEUE_CHECK_TIMER, self.checkLoggingQueue).start()

    def addOutputView(self, command, details):
        if details[ITEM] in self.blockManager.blocks:
            block = self.blockManager.blocks[details[ITEM]]
            block.blockQueue.put(msg.message(msg.MessageType.COMMAND, command, details=details))

    def sendStartupData(self, _):
        mpLogging.info("Sending startup data to the UI that was connected")
        self.uiConnected = True
        details = {}
        # we just want the basic information of the blocks and handlers and not the full information
        # right now it's just sending the code as a dict, but in case we want to send more information
        # then the value of the dict for each code and be updated
        details[BLOCK] = dict(zip(self.getBlocks().keys(), self.getBlocks().keys()))
        details[HANDLER] = dict(zip(self.getHandlers().keys(), self.getHandlers().keys()))
        m = msg.message(msg.MessageType.UI_UPDATE, msg.UiUpdateType.STARTUP, details=details)

        # We want the startup message to be processed first so we add it to the start
        self.pendingUiMessages.insert(0, m)
        self.sendPendingUiMessages()

        # Want to start periodically checking UI status to make sure it is still there
        # Passing in None as the command arg
        threading.Timer(UI_STATUS_CHECK_TIMER, self.isUiConnected).start()

    def isUiConnected(self):
        # If the ui has responded at one point and then not for a while we're going to say it's disconnected
        # This will cause message to be sent to ui to be stored in pending messages
        # once the ui is reconnected we'll send the pending messages on one message
        # so as to not clog the queue
        if self.uiLastTime and time.time() - self.uiLastTime > UI_STATUS_CHECK_TIMER * 3:
            self.uiConnected = False
        else:
            threading.Timer(UI_STATUS_CHECK_TIMER, self.isUiConnected).start()

    def startRouter(self):
        self.routerProcess = dillMp.Process(target=mpLogging.loggedProcess,
                                            args=(self.loggingQueue, "router", self.messageRouter.initAndStartLoop),
                                            name="Router")
        # self.routerProcess = Process(target=self.messageRouter.initAndStartLoop, name="Router")
        self.routerProcess.start()

    def cmdStart(self, _, details=None):
        # Called by command processor on receiving the start command message
        if self.routerProcess is None:
            self.startRouter()

        for code, block in self.blockManager.blocks.items():
            if code not in self.processDict:
                self.startBlockProcess(code, block)
            else:
                print("Error Running Block: " + code)

        threading.Timer(STATUS_CHECK_TIMER, self.checkItemStatus).start()

    def runBlock(self, code):
        if self.routerProcess is None:
            self.startRouter()

        if code in self.blockManager.blocks and code not in self.processDict:
            block = self.blockManager.blocks[code]
            self.startBlockProcess(code, block)
        else:
            print("Error Running Block: " + code)

    def startBlockProcess(self, code, block):
        processName = "Block-" + str(code)
        # blockProcess = Process(target=mpLogging.loggedProcess
        # block.start, name=processName)
        blockProcess = dillMp.Process(target=mpLogging.loggedProcess,
                                      args=(self.loggingQueue, code, block.start),
                                      name=processName)

        self.processDict[code] = blockProcess
        blockProcess.start()

    def cmdEnd(self, _, details=None):
        # Called by command processor on receiving the end command message
        while self.processDict:
            for key, p in self.processDict.items():
                p.join(.5)
                if p.exitcode is not None:
                    del self.processDict[key]
        self.routerProcess.join()

    def endBlock(self, code, timeout=None):
        if code in self.processDict:
            if timeout:
                self.processDict[code].join(timeout)
            else:
                self.processDict[code].close()
            del self.processDict[code]

    def getBlocks(self):
        return self.blockManager.blocks

    def getHandlers(self):
        return self.handlerManager.handlers

    def loadBlockConfig(self, config):
        if config:
            configDict = self.loader.loadAndReplaceYamlFile(config)
            self.blockManager.loadBlocks(configDict)

    def loadHandlerConfig(self, config):
        if config:
            configDict = self.loader.loadAndReplaceYamlFile(config)
            self.handlerManager.loadHandlers(configDict)

    def loadConfigs(self, blockConfig, handlerConfig):
        self.loadBlockConfig(blockConfig)
        self.loadHandlerConfig(handlerConfig)
