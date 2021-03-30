
from .mainframe import mainframe

from .ui.mainWindow import mainWindow

from PySide6 import QtWidgets
import threading


def start():
    # init starter variables
    main = mainframe()
    mainframeThread = threading.Thread(target=main.start)
    mainframeThread.start()
    # main.runManagerAndRouter()
    app = QtWidgets.QApplication([])

    mainWindow(main)

    app.exec_()
