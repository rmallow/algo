from .outputView import outputView
from .uiSettings import OUTPUT_VIEW_FEED_UI_FILE

from .util import loadingUtil

from ..commonUtil import pathUtil

from PySide6 import QtGui, QtCore


class outputViewFeed(outputView):
    def __init__(self, outputViewModel, parent=None):
        super().__init__(outputViewModel, parent)

        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + OUTPUT_VIEW_FEED_UI_FILE, parent=self)

        self.setup()
        """
        self.model = QtGui.QStandardItemModel()
        for i in range(0, 20):
            self.model.appendRow(QtGui.QStandardItem("test row: " + str(i)))
        """
        self.ui.tableView.setModel(self.outputViewModel)

    @QtCore.Slot()
    def updateOnLoad(self):
        pass
        # Table has some weird graphical glitch where it's not loading properly
        # Lazy way to get around this as no other easy solution worked well is this
        # self.outputViewModel.insertRow(0, QtGui.QStandardItem(""))
        # self.outputViewModel.takeRow(0)
