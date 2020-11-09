import algo.message as msg
import logging

"""
used by classes that need to process commands
default commands are start, end, abort and resume
these funcs will need to be overwritten by child class

"""

class commandProcessor():
    def __init__(self):
        #get copy of the dict so can make changes later
        self.m_cmdDict = dict(CMD_DICT)

    def removeCmdFunc(self, key):
        self.m_cmdDict.pop(key,None)

    def addCmdFunc(self, key, func, overwrite = False):
        if key not in self.m_cmdDict or overwrite:
            self.m_cmdDict[key] = func

    def cmdNotFound(self, message):
        logging.error("command not found")
        logging.error(str(message))

    def cmdStart(self,message):
        self.cmdStart(message)

    def cmdEnd(self,message):
        self.cmdEnd(message)

    def cmdAbort(self,message):
        self.cmdAbort(message)

    def cmdResume(self,message):
        self.cmdResume(message)

    def processCommand(self, message):
        self.m_cmdDict.get(message.m_message,commandProcessor.cmdNotFound)(self,message)

CMD_DICT = {
    msg.COMMAND_START: commandProcessor.cmdStart,
    msg.COMMAND_END: commandProcessor.cmdEnd,
    msg.COMMAND_ABORT: commandProcessor.cmdAbort,
    msg.COMMAND_RESUME: commandProcessor.cmdResume
}