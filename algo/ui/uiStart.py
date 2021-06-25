from .mainWindow import mainWindow

from PySide6 import QtWidgets


def start():
    app = QtWidgets.QApplication([])

    mainWindow()

    app.exec_()
