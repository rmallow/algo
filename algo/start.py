
from .mainframe import mainframe

from .commonUtil import errorHandling

import threading
from queue import Queue


def start(clArgs):
    uiArgPresent = False
    uiQueue = None
    if "-u" in clArgs:
        uiArgPresent = True
        uiQueue = Queue()
    # init starter variables
    main = mainframe(uiQueue)
    mainframeThread = threading.Thread(target=main.start)
    mainframeThread.start()

    # If ui arg passed in then start, otherwise do not import
    if uiArgPresent:
        try:
            from .ui import uiStart
        except ModuleNotFoundError:
            errorHandling.logAssert("UI command arg passes (-u) but ui modules not installed",
                                    description="Make to install ui requirements to run ui")
        else:
            uiStart.start(main)
