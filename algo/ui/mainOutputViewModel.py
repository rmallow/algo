from .uiSettings import OUTPUT_TYPES

from PySide6 import QtGui, QtCore


class mainOutputViewModel():
    def __init__(self, mainframe):

        # Is it not confusing that QStandardItemModel is in QtGui
        # yet other models are all in QtCore???
        # who's responsible for this weird organization
        self.blockComboModel = QtGui.QStandardItemModel()
        self.handlerComboModel = QtGui.QStandardItemModel()

        self.addBlocks(mainframe.getBlocks())
        self.addHandlers(mainframe.getHandlers())

        # All output Types are already known at runtime
        # But availability is determined per item
        self.typeModel = QtCore.QStringListModel(OUTPUT_TYPES)

    def addItem(self, model, key, value):
        item = QtGui.QStandardItem(str(key))
        item.setData(value)
        model.appendRow(item)

    def addBlocks(self, blockDict):
        for key, value in blockDict.items():
            self.addItem(self.blockComboModel, key, value)

    def addHandlers(self, handlerDict):
        for key, value in handlerDict.items():
            self.addItem(self.handlerComboModel, key, value)
