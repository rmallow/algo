
from .mainframe import mainframe

from .ui.mainWindow import mainWindow
from PySide6 import QtWidgets
import sys


def start():
    # init starter variables
    main = mainframe()
    # main.runManagerAndRouter()
    app = QtWidgets.QApplication([])

    window = mainWindow()
    window.loadBlocks(main.getBlocks())
    window.loadHandlers(main.getHandlers())

    window.runAllSignal.connect(main.runAll)
    window.endAllSignal.connect(main.endAll)

    status = app.exec_()

    sys.exit(status)
