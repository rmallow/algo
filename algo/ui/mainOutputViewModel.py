from .uiConstants import outputTypesEnum
from .pandasModel import pandasModel

from ..commonGlobals import ITEM
from ..backEnd import message as msg

from PySide6 import QtGui, QtCore


class mainOutputViewModel():
    def __init__(self, mainframe, mainModel):

        # Is it not confusing that QStandardItemModel is in QtGui
        # yet other models are all in QtCore???
        # who's responsible for this weird organization

        # All selectors will refer back to the same models
        # this way we only need to update one set of models and all selectors will be updated
        self.blockComboModel: QtGui.QStandardItemModel = QtGui.QStandardItemModel()
        self.handlerComboModel: QtGui.QStandardItemModel = QtGui.QStandardItemModel()

        self.addBlocks(mainframe.getBlocks())
        self.addHandlers(mainframe.getHandlers())

        # All output Types are already known at runtime
        # But availability is determined per item
        self.typeModel: QtCore.QStringListModel = QtCore.QStringListModel([val.value for val in outputTypesEnum])

        self.mainModel = mainModel
        self.outputViewModels = {}

        self.mainModel.uiUpdateSignal.connect(self.receiveData)

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
                model.appendDataFrame(data.content)

    def setupOutputView(self, selectionDict):
        """
        Output select has finished selecting output, message mainframe to start sending data
        Return model for output view, mainOutputViewModel owns these models
        """

        m = msg.message(msg.MessageType.COMMAND, msg.CommandType.ADD_OUTPUT_VIEW,
                        details=selectionDict)
        self.mainModel.messageMainframe(m)

        model = pandasModel(**selectionDict)
        modelList = self.outputViewModels.get(selectionDict[ITEM], [])
        modelList.append(model)
        self.outputViewModels[selectionDict[ITEM]] = modelList
        return model
