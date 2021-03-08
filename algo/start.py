
from .mainframe import mainframe

from .ui.mainWindow import mainWindow
from PySide6 import QtWidgets
import sys


def start():
    # init starter variables
    main = mainframe()
    # main.runManagerAndRouter()
    app = QtWidgets.QApplication([])

    mainWindow(main)

    sys.exit(app.exec_())
