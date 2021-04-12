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
        # get copy of the dict so can make changes later
        self.cmdDict = dict(CMD_DICT)

    def removeCmdFunc(self, key):
        """
        @brief: remove command function from command func dict, no longer makes it callable

        @param: key in cmd dict to remove
        """
        self.cmdDict.pop(key, None)

    def addCmdFunc(self, key, func, overwrite=False):
        """
        @brief: add command function from command func dict, no longer makes it callable

        @param: key -   key in cmd dict to add
        @param: func -  to add at key
            rather than passing in self.xyz must pass in className.xyz
        @param: overwrite - bool, whether to overwrite if key already exists
        """
        if key not in self.cmdDict or overwrite:
            self.cmdDict[key] = func

    def cmdNotFound(self, message):
        """
        @brief: default function for if command is not found

        @param: message -   message passed into command func
        """
        logging.error("command not found")
        logging.error(str(message))

    def cmdStart(self, message):
        """
        @brief: default function for start command, will call overwritten function in child class

        @param: message -   message passed into command func
        """
        self.cmdStart(message)

    def cmdEnd(self, message):
        """
        @brief: default function for endt command, will call overwritten function in child class

        @param: message -   message passed into command func
        """
        self.cmdEnd(message)

    def cmdAbort(self, message):
        """
        @brief: default function for abort command, will call overwritten function in child class

        @param: message -   message passed into command func
        """
        self.cmdAbort(message)

    def cmdResume(self, message):
        """
        @brief: default function for resume command, will call overwritten function in child class

        @param: message -   message passed into command func
        """
        self.cmdResume(message)

    def processCommand(self, message):
        """
        @brief: main command processor, calls function based on message value or default func

        @param: message -   message passed into command func
            message.message determines what func to call
        """
        self.cmdDict.get(message.message, commandProcessor.cmdNotFound)(self, message)


"""
Default command dict, copied on commandProcessor initalization
"""
CMD_DICT = {
    msg.CommandType.START: commandProcessor.cmdStart,
    msg.CommandType.END: commandProcessor.cmdEnd,
    msg.CommandType.ABORT: commandProcessor.cmdAbort,
    msg.CommandType.RESUME: commandProcessor.cmdResume
}
