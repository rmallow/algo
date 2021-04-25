
from .mainframe import mainframe

from .commonUtil import errorHandling
import threading


def start(clArgs):
    # init starter variables
    main = mainframe()
    mainframeThread = threading.Thread(target=main.start)
    mainframeThread.start()

    # If ui arg passed in then start, otherwise do not import
    if "-u" in clArgs:
        try:
            from .ui import uiStart
        except ModuleNotFoundError:
            errorHandling.logAssert("UI command arg passes (-u) but ui modules not installed",
                                    description="Make to install ui requirements to run ui")
        else:
            uiStart.start(main)
