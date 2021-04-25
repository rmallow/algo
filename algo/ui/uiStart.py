from .mainWindow import mainWindow

from PySide6 import QtWidgets


def start(mainframe):
    app = QtWidgets.QApplication([])

    mainWindow(mainframe)

    app.exec_()
