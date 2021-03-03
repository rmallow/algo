from .configWindow import configWindow
from .uiSettings import MAIN_WINDOW_UI_FILE

from .util import loadingUtil

from ..commonUtil import pathUtil

from PySide6 import QtWidgets, QtCore


class mainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + MAIN_WINDOW_UI_FILE)

        # Load child windows
        self.m_configWindow = configWindow(self)

        # Set up signal and slots
        self.ui.configButton.clicked.connect(lambda: self.m_configWindow.ui.show())
        self.m_configWindow.ui.loadConfigsButton.clicked.connect(self.slotLoadConfigs)

        self.ui.show()

    @QtCore.Slot()
    def slotLoadConfigs(self):
        print(self.m_configWindow.ui.blockFileLine.text())
        print(self.m_configWindow.ui.handlerFileLine.text())
