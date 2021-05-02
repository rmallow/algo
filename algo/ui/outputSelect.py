from .uiSettings import OUTPUT_SELECT_ITEM_UI_FILE, OUTPUT_SELECT_TYPE_UI_FILE

from .util import loadingUtil

from ..commonUtil import pathUtil

from PySide6 import QtWidgets, QtCore


class outputSelect(QtWidgets.QWidget):
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
            self.fadeStart(self.selectTypeUI, self.selectItemUI)

    @QtCore.Slot()
    def itemSelected(self, text):
        self.item = text
        if "block" in self.sender().objectName():
            self.isBlockItem = True

        if self.isBlockItem:
            self.selectTypeUI.itemLabel.setText("Block: " + str(self.item))
        else:
            self.selectTypeUI.itemLabel.setText("Handler: " + str(self.item))

        self.fadeStart(self.selectItemUI, self.selectTypeUI)

    def fadeStart(self, fromWidget, toWidget):
        self.eff = QtWidgets.QGraphicsOpacityEffect(fromWidget)
        fromWidget.setGraphicsEffect(self.eff)
        self.anim = QtCore.QPropertyAnimation(fromWidget.graphicsEffect(), QtCore.QByteArray("opacity"))
        self.anim.setDuration(500)
        self.anim.setStartValue(1)
        self.anim.setEndValue(0)
        self.anim.setEasingCurve(QtCore.QEasingCurve.Linear)
        self.anim.finished.connect(lambda: self.fadeEnd(fromWidget, toWidget))
        self.anim.start()

    def fadeEnd(self, fromWidget, toWidget):
        self.mainLayout.replaceWidget(fromWidget, toWidget)
        fromWidget.hide()
        toWidget.show()
        self.eff = QtWidgets.QGraphicsOpacityEffect(toWidget)
        toWidget.setGraphicsEffect(self.eff)
        self.anim = QtCore.QPropertyAnimation(toWidget.graphicsEffect(), QtCore.QByteArray("opacity"))
        self.anim.setDuration(500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QtCore.QEasingCurve.Linear)
        self.anim.start()