from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6 import uic
import sys
import os

import my_ftp

class MESSAGE(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("message_windows.ui", self)

        self.txtMessage.setFocus()
        self.btnFile.clicked.connect(self.showFileDialog)

        # self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.btnSend.click()

    def showFileDialog(self):
        file_filter = "All files (*)"
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a file",
            directory=os.getcwd(),
            filter=file_filter,
        )
        print(str(response))  # ('FILE path', 'All files (*)')
        send_file_result = my_ftp.send_file(response[0])
        alert = QMessageBox()  # Thông báo trạng thái gửi file
        alert.setIcon(QMessageBox.Icon.Warning)
        alert.setWindowTitle("Thông báo")
        alert.setText(str(send_file_result))
        alert.exec()

        if send_file_result == "Gửi file thành công":
            self.txtMessage.setText(f'SEND_FILE: "{os.path.basename(response[0])}"')
            self.btnSend.click() # Gửi lên đc ftp server thì gửi tên file để nhận ở các client khác

if __name__ == "__main__":
    app = QApplication(sys.argv)

    MESSAGE = MESSAGE()
    app.exec()
