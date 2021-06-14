from .uiSettings import LOGGING_WINDOW_UI_FILE
from .loggingModel import loggingModel

from ..commonUtil import pathUtil
from .util import loadingUtil

from PySide6 import QtWidgets, QtCore


class loggingWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + LOGGING_WINDOW_UI_FILE)

        self.ui.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        self.loggingModel = loggingModel()

        self.ui.tableView.setModel(self.loggingModel)
