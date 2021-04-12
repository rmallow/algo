from .util import loadingUtil
from .uiSettings import CONFIG_WINDOW_UI_FILE

from ..commonSettings import SETTINGS_FILE

from ..commonUtil import pathUtil

from PySide6 import QtWidgets, QtCore
import configparser
import os


class configWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + CONFIG_WINDOW_UI_FILE)

        # Load defaults
        config = configparser.ConfigParser()
        config.read(SETTINGS_FILE)
        if 'Configs' in config:
            self.ui.blockFileLine.setText(os.path.abspath(config.get('Configs', 'Block', fallback="")))
            self.ui.handlerFileLine.setText(os.path.abspath(config.get('Configs', 'Handler', fallback="")))
            self.defaultDir = config.get('Configs', 'Handler', fallback=None)

        # Set up signals and slots
        self.ui.blockLoadButton.clicked.connect(self.showFileDialog)
        self.ui.handlerLoadButton.clicked.connect(self.showFileDialog)
        self.ui.otherLoadButton.clicked.connect(self.showFileDialog)

    @QtCore.Slot()
    def showFileDialog(self):
        button = self.sender()
        objName = button.objectName()
        fileName = ""
        if objName == 'blockLoadButton':
            fileName = self.ui.blockFileLine.text()
        elif objName == 'handlerLoadButton':
            fileName = self.ui.handlerFileLine.text()
        elif objName == 'otherLoadButton':
            fileName = self.ui.otherFileLine.text()

        if not fileName:
            fileName = os.path.abspath(os.sep)

        newFileTuple = QtWidgets.QFileDialog.getOpenFileName(self, "Open Config File",
                                                             fileName, "Yaml (*.yml)")

        if newFileTuple[0]:
            if objName == 'blockLoadButton':
                self.ui.blockFileLine.setText(newFileTuple[0])
            elif objName == 'handlerLoadButton':
                self.ui.handlerFileLine.setText(newFileTuple[0])
            elif objName == 'otherLoadButton':
                self.ui.otherFileLine.setText(newFileTuple[0])
