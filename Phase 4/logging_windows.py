from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt
from PyQt6 import uic
import sys



class LOGGING(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("logging_windows.ui", self)
        self.show()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.btnEnter.click()
    
    


if __name__ == "__main__":
    app = QApplication(sys.argv)

    LOGGING = LOGGING()
    app.exec()
