from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt
from PyQt6 import uic
import sys


class MESSAGE(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("message_windows.ui", self)
        # self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.btnSend.click()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MESSAGE = MESSAGE()
    app.exec()
