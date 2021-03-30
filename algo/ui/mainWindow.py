from .configWindow import configWindow
from .uiSettings import MAIN_WINDOW_UI_FILE, TEST_OUTPUT_TAB_FILE
from .blockTab import blockTab
from .handlerTab import handlerTab

from .util import loadingUtil

from ..commonUtil import pathUtil

from PySide6 import QtWidgets, QtCore


class mainWindow(QtWidgets.QMainWindow):
    runAllSignal = QtCore.Signal()
    endAllSignal = QtCore.Signal()

    def __init__(self, mainframe, parent=None):
        super().__init__(parent)
        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + MAIN_WINDOW_UI_FILE)

        # Load child windows
        self.m_configWindow = configWindow(self)
        bTab = blockTab(self.ui.tabWidget)
        hTab = handlerTab(self.ui.tabWidget)
        self.ui.tabWidget.addTab(bTab, "Blocks")
        self.ui.tabWidget.addTab(hTab, "Handlers")

        # Set up connections for mainframe
        self.m_mainframe = mainframe
        self.connectMainframe()

        bTab.loadItems(self.m_mainframe.getBlocks())
        bTab.slotItemChanged(bTab.m_itemModel.index(0, 0))
        hTab.loadItems(self.m_mainframe.getHandlers())

        """
        -------------------
        TEST OUTPUT SECTION
        -------------------
        """
        outputTabUi = loadingUtil.loadUiWidget(dirPath + "/" + TEST_OUTPUT_TAB_FILE, parent=self)
        outputTabUi.listView.setModel(self.m_mainframe.m_outputModel)
        self.ui.tabWidget.addTab(outputTabUi, "Output")

        # Set up signal and slots
        self.ui.configButton.clicked.connect(lambda: self.m_configWindow.ui.show())
        self.ui.startAllButton.clicked.connect(self.OnStartAllButtonClicked)
        self.m_configWindow.ui.loadConfigsButton.clicked.connect(self.slotLoadConfigs)
        # self.ui.addBlockButton.clicked.connect(self.slotAddBlock)

        self.ui.show()

    def connectMainframe(self):
        self.updateData()
        self.runAllSignal.connect(self.m_mainframe.runAll)
        self.endAllSignal.connect(self.m_mainframe.endAll)
        self.m_mainframe.dataChanged.connect(self.updateData)

    @QtCore.Slot()
    def updateData(self):
        pass
        # self.ui.blockListWidget.clear()
        # self.ui.handlerListWidget.clear()
        # self.loadBlocks(self.m_mainframe.getBlocks())
        # self.loadHandlers(self.m_mainframe.getHandlers())

    @QtCore.Slot()
    def slotLoadConfigs(self):
        blockConfigFile = self.m_configWindow.ui.blockFileLine.text()
        handlerConfigFile = self.m_configWindow.ui.handlerFileLine.text()
        self.m_mainframe.loadConfigs(blockConfigFile, handlerConfigFile)

    @QtCore.Slot()
    def OnStartAllButtonClicked(self):
        if self.ui.startAllButton.isChecked():
            self.ui.startAllButton.setText("End All")
            self.runAllSignal.emit()
        else:
            self.ui.startAllButton.setText("Start All")
            self.endAllSignal.emit()


"""
    def loadBlocks(self, blocks):
        for code, block in blocks.items():
            self.ui.blockListWidget.addItem(block.m_code)

    def loadHandlers(self, handlers):
        for code, handler in handlers.items():
            self.ui.handlerListWidget.addItem(handler.m_code)
"""
