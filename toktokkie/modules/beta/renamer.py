import qt_renamer
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

class RenamerGui(QMainWindow, qt_renamer.Ui_Renamer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.browse_button.clicked.connect(self.browse_folder)

    def browse_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Test")
        print(directory)

def main():
    app = QApplication(sys.argv)
    form = RenamerGui()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()