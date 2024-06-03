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

        self.txtMessage.setFocus()  # Auto cho con trỏ vô text box để gõ tin nhắn
        self.btnFile.clicked.connect(self.showFileDialog)   # Chọn file để gửi file

        # self.show()

    def keyPressEvent(self, event): # Gõ phím Enter thì nhấn nút btnSend để gửi tin nhắn
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
        send_file_result = my_ftp.send_file(response[0])            # hàm gửi file lên ftp server trong file my_ftp
        
        if send_file_result == "Gửi file thành công":   # Nếu upload file lên FTP Server thành công
            self.txtMessage.setText(f'SEND_FILE: "{os.path.basename(response[0])}"')    #Gõ tên file vô txtMessage
            self.btnSend.click() # Gửi tên file đến các client khác

        alert = QMessageBox()  # Thông báo trạng thái gửi file
        alert.setIcon(QMessageBox.Icon.Warning)
        alert.setWindowTitle("Thông báo")
        alert.setText(str(send_file_result))
        alert.exec()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    MESSAGE = MESSAGE()
    app.exec()
