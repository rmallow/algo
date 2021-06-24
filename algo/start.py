
from .mainframe import mainframe

import logging

import threading
import os


def setEnvVarsMac():
    # Ran into issues with forking, threading, QT, and url requests
    # so we're setting some environment variables to get around this
    # links above each are where i found the solution
    # https://stackoverflow.com/questions/30816565/python-urllib-does-not-work-with-pyqt-multiprocessing
    os.environ["no_proxy"] = "*"
    # https://stackoverflow.com/questions/50168647/multiprocessing-causes-python-to-crash-and-gives-an-error-may-have-been-in-progr
    os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"


def start(clArgs):
    setEnvVarsMac()
    uiArgPresent = False
    if "-u" in clArgs:
        uiArgPresent = True
    # init starter variables
    main = mainframe()
    mainframeThread = threading.Thread(target=main.start)
    mainframeThread.start()

    # If ui arg passed in then start, otherwise do not import
    if uiArgPresent:
        try:
            from .ui import uiStart
        except ModuleNotFoundError:
            logging.critical("UI command arg passes (-u) but ui modules not installed")
        else:
            uiStart.start(main)
    else:
        main.runAll()
