from .configWindow import configWindow
from .uiSettings import MAIN_WINDOW_UI_FILE
from .blockTab import blockTab
from .handlerTab import handlerTab
from .mainOutputView import mainOutputView

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

        oView = mainOutputView(self.ui.tabWidget)
        self.ui.tabWidget.addTab(oView, "Output")

        # Load child windows
        self.configWindow = configWindow(self)
        bTab = blockTab(self.ui.tabWidget)
        hTab = handlerTab(self.ui.tabWidget)
        self.ui.tabWidget.addTab(bTab, "Blocks")
        self.ui.tabWidget.addTab(hTab, "Handlers")

        # Set up connections for mainframe
        self.mainframe = mainframe
        self.connectMainframe()

        bTab.loadItems(self.mainframe.getBlocks())
        bTab.slotItemChanged(bTab.itemModel.index(0, 0))
        hTab.loadItems(self.mainframe.getHandlers())

        # Set up signal and slots
        self.ui.configButton.clicked.connect(lambda: self.configWindow.ui.show())
        self.ui.startAllButton.clicked.connect(self.OnStartAllButtonClicked)
        self.configWindow.ui.loadConfigsButton.clicked.connect(self.slotLoadConfigs)
        # self.ui.addBlockButton.clicked.connect(self.slotAddBlock)

        self.ui.show()

    def connectMainframe(self):
        self.updateData()
        self.runAllSignal.connect(self.mainframe.runAll)
        self.endAllSignal.connect(self.mainframe.endAll)

    @QtCore.Slot()
    def updateData(self):
        pass
        # self.ui.blockListWidget.clear()
        # self.ui.handlerListWidget.clear()
        # self.loadBlocks(self.mainframe.getBlocks())
        # self.loadHandlers(self.mainframe.getHandlers())

    @QtCore.Slot()
    def slotLoadConfigs(self):
        blockConfigFile = self.configWindow.ui.blockFileLine.text()
        handlerConfigFile = self.configWindow.ui.handlerFileLine.text()
        self.mainframe.loadConfigs(blockConfigFile, handlerConfigFile)

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
            self.ui.blockListWidget.addItem(block.code)

    def loadHandlers(self, handlers):
        for code, handler in handlers.items():
            self.ui.handlerListWidget.addItem(handler.code)
"""
