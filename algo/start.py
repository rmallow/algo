
from .mainframe import mainframe

import logging

import argparse
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


def start():
    setEnvVarsMac()

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--ui', help='Start the ui', action='store_true')
    parser.add_argument('-s', '--server', help='Start the server', action='store_true')
    parser.add_argument('-b', '--both', help='Start both ui and server for full local app', action='store_true')
    args, _ = parser.parse_known_args()

    # init server
    if args.server or args.both:
        main = mainframe()
        mainframeThread = threading.Thread(target=main.start)
        mainframeThread.start()

    # If ui arg passed in then start, otherwise do not import
    if args.ui or args.both:
        try:
            from .ui import uiStart
        except ModuleNotFoundError:
            logging.critical("UI command arg passes (-u) but ui modules not installed")
        else:
            # if ui is present we will allow the ui to run it
            uiStart.start()
    else:
        main.runAll()
