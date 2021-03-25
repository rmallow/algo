from .displayTab import displayTab

from PySide6 import QtCore


class handlerTab(displayTab):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui.addButton.setText("Add Handler")
        self.ui.deleteButton.setText("Delete Handler")

    @QtCore.Slot()
    def slotAddButton(self):
        super().slotAddButton()

    @QtCore.Slot()
    def slotDeleteButton(self):
        super().slotDeleteButton()
