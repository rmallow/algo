from .configWindow import configWindow
from .loggingWindow import loggingWindow
from .statusWindow import statusWindow
from .uiSettings import MAIN_WINDOW_UI_FILE
from .blockTab import blockTab
from .handlerTab import handlerTab
from .mainOutputView import mainOutputView
from .mainOutputViewModel import mainOutputViewModel
from .mainModel import mainModel

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

        self.mainModel = mainModel(self)

        # setup main output view model
        self.oViewModel = mainOutputViewModel(self)
        self.mainModel.updateOutputSignal.connect(self.oViewModel.receiveData)
        self.oViewModel.addOutputViewSignal.connect(self.mainModel.messageMainframe)
        self.mainModel.startupSignal.connect(self.oViewModel.onStartupMessage)

        # Create and add output view
        oView = mainOutputView(self.oViewModel, self.ui.tabWidget)
        self.ui.tabWidget.addTab(oView, "Output")

        # Create and connect logging window
        self.loggingWindow = loggingWindow(self)
        self.mainModel.updateLoggingSignal.connect(self.loggingWindow.loggingModel.receiveData)
        self.ui.loggingButton.clicked.connect(lambda: self.loggingWindow.ui.show())

        # Create and connect status window
        self.statusWindow = statusWindow(self)
        self.mainModel.updateStatusSignal.connect(self.statusWindow.statusModel.receiveData)
        self.ui.statusButton.clicked.connect(lambda: self.statusWindow.ui.show())

        # Create config window
        self.configWindow = configWindow(self)

        # Load Block and Handler view
        bTab = blockTab(self.ui.tabWidget)
        hTab = handlerTab(self.ui.tabWidget)
        self.ui.tabWidget.addTab(bTab, "Blocks")
        self.ui.tabWidget.addTab(hTab, "Handlers")

        # Set up signal and slots

        # For mysterious reasons this signal slot cannot be deleted for the rest of the UI to work
        # After brief investigation I have no idea why this is the case
        self.ui.configButton.clicked.connect(lambda: self.configWindow.ui.show())
        # Spooky, noted to fix in later development

        self.ui.startAllButton.clicked.connect(self.OnStartAllButtonClicked)
        self.configWindow.ui.loadConfigsButton.clicked.connect(self.slotLoadConfigs)

        self.ui.show()

    @QtCore.Slot()
    def slotLoadConfigs(self):
        pass
        # blockConfigFile = self.configWindow.ui.blockFileLine.text()
        # handlerConfigFile = self.configWindow.ui.handlerFileLine.text()
        # tell mainframe to load configs

    @QtCore.Slot()
    def OnStartAllButtonClicked(self):
        if self.ui.startAllButton.isChecked():
            self.ui.startAllButton.setText("End All")
            self.runAllSignal.emit()
        else:
            self.ui.startAllButton.setText("Start All")
            self.endAllSignal.emit()
