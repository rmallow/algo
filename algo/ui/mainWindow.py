from .configWindow import configWindow
from .uiSettings import MAIN_WINDOW_UI_FILE

from .util import loadingUtil

from ..commonUtil import pathUtil

from PySide6 import QtWidgets, QtCore


class mainWindow(QtWidgets.QMainWindow):
    def __init__(self, mainframe, parent=None):
        super().__init__(parent)
        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + MAIN_WINDOW_UI_FILE)

        self.m_mainframe = mainframe

        for block in self.m_mainframe.m_blockManager.m_blocks:
            self.ui.blockListWidget.addItem(block.m_code)

        for handler in self.m_mainframe.m_handlerManager.m_handlers:
            self.ui.handlerListWidget.addItem(handler.m_code)
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
