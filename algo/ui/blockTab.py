from .displayTab import displayTab


class blockTab(displayTab):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui.addButton.setText("Add Block")
        self.ui.deleteButton.setText("Delete Block")
