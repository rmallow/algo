from .uiSettings import MAIN_OUTPUT_VIEW_UI_FILE
from .outputSelect import outputSelect
from .outputViewFeed import outputViewFeed
from .uiConstants import outputTypesEnum

from .util import loadingUtil, animations

from ..commonGlobals import TYPE
from ..commonUtil import pathUtil
# from ..commonUtil import errorHandling

from PySide6 import QtWidgets, QtCore


class mainOutputView(QtWidgets.QWidget):
    def __init__(self, mainOutputViewModel, parent=None):
        super().__init__(parent)

        self.mainOutputViewModel = mainOutputViewModel

        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + MAIN_OUTPUT_VIEW_UI_FILE, parent=self)

        self.mainLayout = QtWidgets.QVBoxLayout(self.ui.scrollAreaWidgetContents)
        self.mainLayout.setSpacing(0)

        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        self.ui.scrollAreaWidgetContents.setLayout(self.mainLayout)

        windowSize = self.ui.size()
        self.ui.scrollArea.resize(windowSize.width()-8, windowSize.height())

        self.initButtons()

        # manually call slot to insert first selector at startup
        self.addButtonClicked()

        self.mainLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,
                                                            QtWidgets.QSizePolicy.Expanding))
        self.mainLayout.addSpacing(self.ui.height()/8)

    def initButtons(self):
        self.buttonWidget = QtWidgets.QWidget(self.ui.scrollAreaWidgetContents)
        self.buttonWidget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        horizLayout = QtWidgets.QHBoxLayout()
        horizLayout.setSpacing(0)

        addButton = QtWidgets.QPushButton("+")
        addButton.setMaximumWidth(30)
        addButton.setMaximumHeight(30)

        addButton.clicked.connect(self.addButtonClicked)

        subButton = QtWidgets.QPushButton("-")
        subButton.setMaximumWidth(30)
        subButton.setMaximumHeight(30)

        subButton.clicked.connect(self.subButtonClicked)

        self.buttonWidget.setMaximumHeight(addButton.height() + 10)

        horizLayout.addWidget(addButton)
        horizLayout.addWidget(subButton)
        horizLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,
                                                        QtWidgets.QSizePolicy.Expanding))

        self.buttonWidget.setLayout(horizLayout)

        self.mainLayout.addWidget(self.buttonWidget)

    def addButtonClicked(self):
        index = self.mainLayout.indexOf(self.buttonWidget)
        selector = outputSelect(self.mainOutputViewModel)
        selector.selectionFinished.connect(self.onSelectionFinished)
        self.mainLayout.insertWidget(index, selector)

    def subButtonClicked(self):
        index = self.mainLayout.indexOf(self.buttonWidget)
        if index > 1:
            item = self.mainLayout.takeAt(index - 1)
            if item:
                w = item.widget()
                if w:
                    w.deleteLater()

    @QtCore.Slot()
    def onSelectionFinished(self, selectionSettings):
        """
        Output select is finished, send settings to mainOutputViewModel to translate to message
        """
        outputViewModel = self.mainOutputViewModel.setupOutputView(selectionSettings)
        oView = None
        slot = None
        if selectionSettings[TYPE] == outputTypesEnum.FEED.value:
            oView = outputViewFeed(outputViewModel, selectionSettings, self)
            slot = oView.updateOnLoad

        animations.fadeStart(self, self.sender(), oView, self.mainLayout, finishedSlot=slot)
