from . import message as msg
import logging

"""
used by classes that need to process commands
default commands are start, end, abort and resume
these funcs will need to be overwritten by child class

TODO: add customizable default command
"""

class commandProcessor():
    def __init__(self):
        #get copy of the dict so can make changes later
        self.m_cmdDict = dict(CMD_DICT)

    """
    @brief: remove command function from command func dict, no longer makes it callable

    @param: key in cmd dict to remove
    """
    def removeCmdFunc(self, key):
        self.m_cmdDict.pop(key,None)

    """
    @brief: add command function from command func dict, no longer makes it callable

    @param: key -   key in cmd dict to add
    @param: func -  to add at key
        rather than passing in self.xyz must pass in className.xyz
    @param: overwrite - bool, whether to overwrite if key already exists
    """
    def addCmdFunc(self, key, func, overwrite = False):
        if key not in self.m_cmdDict or overwrite:
            self.m_cmdDict[key] = func

    """
    @brief: default function for if command is not found

    @param: message -   message passed into command func
    """
    def cmdNotFound(self, message):
        logging.error("command not found")
        logging.error(str(message))

    """
    @brief: default function for start command, will call overwritten function in child class

    @param: message -   message passed into command func
    """
    def cmdStart(self,message):
        self.cmdStart(message)

    """
    @brief: default function for endt command, will call overwritten function in child class

    @param: message -   message passed into command func
    """
    def cmdEnd(self,message):
        self.cmdEnd(message)

    """
    @brief: default function for abort command, will call overwritten function in child class

    @param: message -   message passed into command func
    """
    def cmdAbort(self,message):
        self.cmdAbort(message)

    """
    @brief: default function for resume command, will call overwritten function in child class

    @param: message -   message passed into command func
    """
    def cmdResume(self,message):
        self.cmdResume(message)

    """
    @brief: main command processor, calls function based on message value or default func

    @param: message -   message passed into command func 
        message.m_message determines what func to call
    """
    def processCommand(self, message):
        self.m_cmdDict.get(message.m_message,commandProcessor.cmdNotFound)(self,message)


"""
Default command dict, copied on commandProcessor initalization
"""
CMD_DICT = {
    msg.CommandType.START: commandProcessor.cmdStart,
    msg.CommandType.END: commandProcessor.cmdEnd,
    msg.CommandType.ABORT: commandProcessor.cmdAbort,
    msg.CommandType.RESUME: commandProcessor.cmdResume
}