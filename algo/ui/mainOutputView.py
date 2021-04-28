from .uiSettings import MAIN_OUTPUT_VIEW_UI_FILE

from .util import loadingUtil

from ..commonUtil import pathUtil
# from ..commonUtil import errorHandling

from PySide6 import QtWidgets


class mainOutputView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + MAIN_OUTPUT_VIEW_UI_FILE, parent=self)
    
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.addButtons()

        self.mainLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,
                                                            QtWidgets.QSizePolicy.Expanding))

        self.ui.scrollArea.setLayout(self.mainLayout)

    def addButtons(self):
        buttonWidget = QtWidgets.QWidget(self.ui.scrollArea)
        # This line probably won't work on different sized screens
        buttonWidget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        
        horizLayout = QtWidgets.QHBoxLayout()
        horizLayout.setSpacing(0)
        
        addButton = QtWidgets.QPushButton("+")
        addButton.setMaximumWidth(30)
        addButton.setMaximumHeight(30)

        subButton = QtWidgets.QPushButton("-")
        subButton.setMaximumWidth(30)
        subButton.setMaximumHeight(30)

        buttonWidget.setMaximumHeight(addButton.height() + 10)

        horizLayout.addWidget(addButton)
        horizLayout.addWidget(subButton)
        horizLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,
                                                        QtWidgets.QSizePolicy.Expanding))

        buttonWidget.setLayout(horizLayout)
        
        self.mainLayout.addWidget(buttonWidget)