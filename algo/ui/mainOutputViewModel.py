from .uiConstants import outputTypesEnum
from .pandasModel import pandasModel

from ..commonGlobals import ITEM, BLOCK, HANDLER
from ..backEnd import message as msg

from PySide6 import QtGui, QtCore


class mainOutputViewModel(QtCore.QObject):
    addOutputViewSignal = QtCore.Signal(msg.message)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Is it not confusing that QStandardItemModel is in QtGui
        # yet other models are all in QtCore???
        # who's responsible for this weird organization

        # All selectors will refer back to the same models
        # this way we only need to update one set of models and all selectors will be updated
        self.blockComboModel: QtGui.QStandardItemModel = QtGui.QStandardItemModel()
        self.handlerComboModel: QtGui.QStandardItemModel = QtGui.QStandardItemModel()

        # All output Types are already known at runtime
        # But availability is determined per item
        self.typeModel: QtCore.QStringListModel = QtCore.QStringListModel([val.value for val in outputTypesEnum])

        self.outputViewModels = {}

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

    def receiveData(self, data: msg.message):
        if data.key.sourceCode in self.outputViewModels:
            modelList = self.outputViewModels[data.key.sourceCode]
            for model in modelList:
                model.appendDataFrame(data.details)

    def setupOutputView(self, selectionDict):
        """
        Output select has finished selecting output, message mainframe to start sending data
        Return model for output view, mainOutputViewModel owns these models
        """

        m = msg.message(msg.MessageType.COMMAND, msg.CommandType.ADD_OUTPUT_VIEW,
                        details=selectionDict)

        self.addOutputViewSignal.emit(m)

        model = pandasModel(**selectionDict)
        modelList = self.outputViewModels.get(selectionDict[ITEM], [])
        modelList.append(model)
        self.outputViewModels[selectionDict[ITEM]] = modelList
        return model

    @QtCore.Slot()
    def onStartupMessage(self, message: msg.message):
        """ On startup message add blocks and handlers to their combo models """
        self.blockComboModel.clear()
        self.handlerComboModel.clear()
        if message.details:
            if BLOCK in message.details:
                self.addBlocks(message.details[BLOCK])
            if HANDLER in message.details:
                self.addHandlers(message.details[HANDLER])
