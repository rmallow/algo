
from .mainframe import mainframe

from .ui.mainWindow import mainWindow
from PySide6 import QtWidgets
import sys


def start():

    if True:
        # init starter variables
        main = mainframe()
        main.runManagerAndRouter()
    else:
        app = QtWidgets.QApplication([])

        mainWindow()

        sys.exit(app.exec_())
