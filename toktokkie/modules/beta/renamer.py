import os
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QTreeWidgetItem, QHeaderView

from toktokkie.modules.beta.qt_renamer import Ui_Renamer
from utils.renaming.TVSeriesRenamer import Renamer


class RenamerGui(QMainWindow, Ui_Renamer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.renamer = None
        self.setupUi(self)
        self.browse_button.clicked.connect(self.browse_folder)
        self.fetch_button.clicked.connect(self.fetch)
        self.cancel_button.clicked.connect(self.cancel)
        self.confirm_button.clicked.connect(self.confirm)
        self.changelist.header().setSectionResizeMode(0, QHeaderView.Stretch)

        self.confirmation = []

    def browse_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Test")
        self.directory_path_edit.setText(directory)

    def fetch(self):

        if len(self.confirmation) > 0 or self.renamer is not None:
            return

        path = self.directory_path_edit.toPlainText()
        if not os.path.isdir(path):

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("The entered path is not a valid, existing directory")
            msg.setWindowTitle("Not A directory")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        self.renamer = Renamer(path)                        # Create a new Renamer object
        self.confirmation = self.renamer.request_confirmation()  # Request the confirmation dictionary from the Renamer

        for item in self.confirmation:
            self.changelist.addTopLevelItem(QTreeWidgetItem([item.old_name, item.new_name]))

    def cancel(self):
        self.changelist.clear()
        self.renamer = None
        self.confirmation = []

    def confirm(self):

        for item in self.confirmation:
            item.confirmed = True

        self.renamer.confirm(self.confirmation)
        self.renamer.start_rename()
        self.cancel()

def main():
    app = QApplication(sys.argv)
    form = RenamerGui()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()