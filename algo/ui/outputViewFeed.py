from .outputView import outputView
from .uiSettings import OUTPUT_VIEW_FEED_UI_FILE

from .util import loadingUtil

from ..commonUtil import pathUtil

from PySide6 import QtGui, QtCore


class outputViewFeed(outputView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Load UI file
        dirPath = pathUtil.getFileDirPath(__file__)
        self.ui = loadingUtil.loadUiWidget(dirPath + "/" + OUTPUT_VIEW_FEED_UI_FILE, parent=self)

        self.setup()

        self.model = QtGui.QStandardItemModel()
        for i in range(0, 20):
            self.model.appendRow(QtGui.QStandardItem("test row: " + str(i)))
        self.ui.tableView.setModel(self.model)

    @QtCore.Slot()
    def updateOnLoad(self):
        # Table has some weird graphical glitch where it's not loading properly
        # Lazy way to get around this as no other easy solution worked well is this
        self.model.insertRow(0, QtGui.QStandardItem(""))
        self.model.takeRow(0)
