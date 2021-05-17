from .uiSettings import OUTPUT_SELECT_ITEM_UI_FILE, OUTPUT_SELECT_TYPE_UI_FILE

from .util import loadingUtil, animations

from ..commonGlobals import TYPE, ITEM
from ..commonUtil import pathUtil

from PySide6 import QtWidgets, QtCore


class outputSelect(QtWidgets.QWidget):
    selectionFinished = QtCore.Signal(dict)

    def __init__(self, model):
        super().__init__()

        self.model = model
        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.selectItemUI = loadingUtil.loadUiWidget(dirPath + "/" + OUTPUT_SELECT_ITEM_UI_FILE)
        self.selectTypeUI = loadingUtil.loadUiWidget(dirPath + "/" + OUTPUT_SELECT_TYPE_UI_FILE)

        self.initSelectItem()
        self.initSelectType()

        self.mainLayout = QtWidgets.QVBoxLayout()

        self.backButtonSetup()

        self.mainLayout.addWidget(self.selectItemUI)
        self.mainLayout.setSpacing(0)

        self.setLayout(self.mainLayout)
        self.show()

        self.item = None
        self.isBlockItem = False
        self.outputType = None

    def initSelectItem(self):
        self.selectItemUI.blockComboBox.setModel(self.model.blockComboModel)
        self.selectItemUI.blockComboBox.setCurrentIndex(-1)
        self.selectItemUI.blockComboBox.textActivated.connect(self.itemSelected)

        self.selectItemUI.handlerComboBox.setModel(self.model.handlerComboModel)
        self.selectItemUI.handlerComboBox.setCurrentIndex(-1)
        self.selectItemUI.handlerComboBox.textActivated.connect(self.itemSelected)

    def initSelectType(self):
        self.selectTypeUI.typeComboBox.setModel(self.model.typeModel)
        self.selectTypeUI.typeComboBox.setCurrentIndex(-1)
        self.selectTypeUI.typeComboBox.textActivated.connect(self.typeSelected)

    def backButtonSetup(self):
        backWidget = QtWidgets.QWidget(self)
        backLayout = QtWidgets.QHBoxLayout()
        # Unicode for a left arrow U+2190
        self.backButton = QtWidgets.QPushButton("\u2190", backWidget)
        self.backButton.clicked.connect(self.backButtonClicked)
        backLayout.addWidget(self.backButton)
        backLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,
                                                       QtWidgets.QSizePolicy.Expanding))
        backWidget.setLayout(backLayout)
        backWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.mainLayout.addWidget(backWidget)

    def backButtonClicked(self):
        if self.mainLayout.indexOf(self.selectItemUI) != -1:
            pass
        elif self.mainLayout.indexOf(self.selectTypeUI) != -1:
            animations.fadeStart(self, self.selectTypeUI, self.selectItemUI, self.mainLayout)

    @QtCore.Slot()
    def itemSelected(self, text):
        self.item = text
        self.isBlockItem = "block" in self.sender().objectName()

        if self.isBlockItem:
            self.selectTypeUI.itemLabel.setText("Block: " + str(self.item))
            self.selectItemUI.handlerComboBox.setCurrentIndex(-1)
        else:
            self.selectTypeUI.itemLabel.setText("Handler: " + str(self.item))
            self.selectItemUI.blockComboBox.setCurrentIndex(-1)

        animations.fadeStart(self, self.selectItemUI, self.selectTypeUI, self.mainLayout)

    @QtCore.Slot()
    def typeSelected(self, text):
        self.selectionFinished.emit({TYPE: text, ITEM: self.item})
