from .configWindow import configWindow
from .uiSettings import MAIN_WINDOW_UI_FILE

from .util import loadingUtil

from ..commonUtil import pathUtil

from PySide6 import QtWidgets, QtCore


class mainWindow(QtWidgets.QMainWindow):
    runAllSignal = QtCore.Signal()
    endAllSignal = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + MAIN_WINDOW_UI_FILE)

        # Load child windows
        self.m_configWindow = configWindow(self)

        # Set up signal and slots
        self.ui.configButton.clicked.connect(lambda: self.m_configWindow.ui.show())
        self.ui.startAllButton.clicked.connect(self.OnStartAllButtonClicked)
        self.m_configWindow.ui.loadConfigsButton.clicked.connect(self.slotLoadConfigs)

        self.ui.show()

    def loadBlocks(self, blocks):
        for code, block in blocks.items():
            self.ui.blockListWidget.addItem(block.m_code)

    def loadHandlers(self, handlers):
        for code, handler in handlers.items():
            self.ui.handlerListWidget.addItem(handler.m_code)

    @QtCore.Slot()
    def slotLoadConfigs(self):
        print(self.m_configWindow.ui.blockFileLine.text())
        print(self.m_configWindow.ui.handlerFileLine.text())

    @QtCore.Slot()
    def OnStartAllButtonClicked(self):
        if self.ui.startAllButton.isChecked():
            self.ui.startAllButton.setText("End All")
            self.runAllSignal.emit()
        else:
            self.ui.startAllButton.setText("Start All")
            self.endAllSignal.emit()
