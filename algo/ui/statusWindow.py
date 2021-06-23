from .uiSettings import STATUS_WINDOW_UI_FILE
from .statusModel import statusModel

from .util import loadingUtil

from ..commonUtil import pathUtil

from PySide6 import QtWidgets, QtCore


class statusWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Load UI file and setup
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + STATUS_WINDOW_UI_FILE)
        self.ui.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        self.statusModel = statusModel()
        self.ui.processView.setModel(self.statusModel)
