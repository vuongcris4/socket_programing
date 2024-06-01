from PyQt6.QtWidgets import QApplication, QMessageBox, QListWidgetItem
from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt

from logging_windows import LOGGING
from message_windows import MESSAGE

import socket
from time import sleep
import my_ftp

HEADER = 64
PORT = 8000
FORMAT = "UTF-8"
DISCONNECT_MESSAGE = "!exit"
SERVER = "localhost"
ADDR = (SERVER, PORT)

client = ""
connected = False


# Tạo một thread mới song song Main Thread để connect to server, kiểm tra kết nối, nhận gói tin
class Connect_ReceiveMessage(QThread):
    gui_tin_hieu = pyqtSignal(str)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        global client

        global connected
        connected = False

        global received_msg

        while True:
            try:
                if connected == False:  # Nếu kết nối lỗi (realtime check)
                    client = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM
                    )  # ipv4, TCP
                    client.connect(ADDR)
                    client.send(NAME.encode(FORMAT))  # Gửi riêng NAME tới server trước
                    received_msg = client.recv(HEADER).decode(FORMAT)
                    if received_msg != "":
                        connected = True
                        self.gui_tin_hieu.emit(f'Kết nối tới "{SERVER}" thành công')
                    sleep(2)
            except Exception as e:
                # error_message = f"An error occurred: {e}"
                error_message = f"....Đang cố gắng kết nối tới server....."
                self.gui_tin_hieu.emit(error_message)
                connected = False
                sleep(1)

            if connected == True:  # Kết nối thành công thì nhận gói tin
                try:
                    received_msg = client.recv(HEADER).decode(FORMAT)  # GÓI TIN CẦN TÌM
                    # item = QListWidgetItem(
                    #     str(received_msg)
                    # )  # Add từng item kiểu này để scroll xuống được
                    self.ui.message.lstMessage.addItem(received_msg)
                    sleep(0.1)  # Add xong cần một tí thời gian mới scrollDown được
                    self.ui.message.lstMessage.scrollToBottom()
                    # print(received_msg)

                    if received_msg == "":  # Nếu trả về gói tin rỗng thì server bị tắt
                        self.gui_tin_hieu.emit("Lỗi server")
                        connected = False
                        sleep(1)

                    if "SEND_FILE" in received_msg: # Nếu client khác gửi file thì nhận file
                        file_name = received_msg[received_msg.find('"') + 1 : received_msg.rfind('"')] # Lấy tên file
                        person = received_msg[:received_msg.index(':')] # Tên người gửi

                        local_name = f"{person}_{file_name}"  # NAME_tên file
                        my_ftp.receive_file(local_name, file_name)

                except ConnectionResetError:  # Server bị tắt thì gặp lỗi này
                    self.gui_tin_hieu.emit("Server đã bị tắt")
                    connected = False
                    sleep(3)


class UI:
    def __init__(self):
        self.logging = LOGGING()
        self.message = MESSAGE()

        self.logging.show()
        self.logging.btnEnter.clicked.connect(lambda: self.changeUI("message"))
        # self.logging.btnEnter.setShortcut('Enter')
        # btnSend  txtMessage lstMessage
        self.message.btnSend.clicked.connect(self.send_message)

    def changeUI(self, i):
        if i == "message":
            self.logging.hide()
            global NAME
            NAME = self.logging.txtName.text()
            self.message.lbName.setText(NAME)
            self.message.show()
            self.init_connect()  # Khởi tạo kết nối tới server với tên NAME

    def init_connect(self):
        self.connection_thread = Connect_ReceiveMessage(self)
        self.connection_thread.gui_tin_hieu.connect(self.message.lbAnnouce.setText)
        self.connection_thread.start()

    def send_message(self):
        msg = self.message.txtMessage.text()
        # if message:  # Chỉ gửi tin nhắn nếu có nội dung
        # send_thread = SendMessageThread(message)
        # send_thread.send_signal.connect(self.handle_send_result)
        # send_thread.start()
        # print(msg)
        if connected and msg != "":
            item = QListWidgetItem(
                "\t" * 4 + "[Tôi]: " + msg
            )  # Add từng item kiểu này để scroll xuống được
            self.message.lstMessage.addItem(item)  # align right
            self.message.lstMessage.scrollToItem(item)
            self.message.txtMessage.setText("")
        try:
            if msg != "":
                send(f"[{NAME}]: {msg}")  # SEND NAME (nhập từ bàn phím), msg
        except Exception as e:
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Icon.Warning)
            alert.setWindowTitle("Thông báo")
            alert.setText("Chưa kết nối tới server")
            alert.exec()


def send(msg):
    message = msg.encode(FORMAT)
    message += b" " * (HEADER - len(message))  # Thêm dấu cách cho đủ 64 byte
    client.send(message)


if __name__ == "__main__":
    app = QApplication([])
    ui = UI()
    app.exec()
