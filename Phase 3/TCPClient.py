from PyQt6.QtWidgets import QApplication, QMessageBox, QListWidgetItem
from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt

from logging_windows import LOGGING
from message_windows import MESSAGE


import socket
import threading
from time import sleep

HEADER = 1024
PORT = 8003
FORMAT = "UTF-8"
SERVER = "localhost"
ADDR = (SERVER, PORT)


connected = False
client = ""


class Connect_ReceiveMessage(QThread):
    gui_tin_hieu = pyqtSignal(str)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        global connected, client
        while True:
            if connected == False:
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4, TCP
                    client.connect(ADDR)
                    client.send(NAME.encode(FORMAT))
                    connected = True
                    self.gui_tin_hieu.emit(f"Kết nối tới {SERVER} thành công!")

                except ConnectionRefusedError as e:
                    self.gui_tin_hieu.emit("...Đang cố gắng kết nối tới server....")
                    connected = False
                    sleep(1)

            if connected == True:
                try:
                    msg = client.recv(HEADER).decode(FORMAT)
                    if not msg:
                        self.gui_tin_hieu.emit("Server đã bị tắt")
                        connected = False 
                    
                    self.ui.message.lstMessage.addItem(msg) # add message
                    sleep(0.1)
                    self.ui.message.lstMessage.scrollToBottom()

                    sleep(0.1)
                except Exception:
                    self.gui_tin_hieu.emit("Server đã bị tắt")
                    connected = False
                    sleep(1)

class UI:
    def __init__(self):
        self.logging = LOGGING()
        self.message = MESSAGE()

        self.logging.show()
        self.logging.btnEnter.clicked.connect(lambda: self.changeUI("message"))

        self.message.btnSend.clicked.connect(self.handle_send)
    
    def changeUI(self, i):
        if i == "message":
            global NAME
            NAME = self.logging.txtName.text()
            self.message.lbName.setText(NAME)
            self.logging.hide()
            self.message.show()
            self.init_connect()
    
    def init_connect(self):
        self.connection_thread = Connect_ReceiveMessage(self)
        self.connection_thread.gui_tin_hieu.connect(self.message.lbAnnouce.setText)
        self.connection_thread.start()

    

    def handle_send(self):
        msg = self.message.txtMessage.text()
        self.message.txtMessage.setText("")

        if connected and msg != "":
            item = QListWidgetItem("\t"*4 + "[Tôi]: " +msg)
            self.message.lstMessage.addItem(item)
            self.message.lstMessage.scrollToBottom()

        try:
            if msg!= "":
                send_msg(f"[{NAME}]: {msg}")  # SEND NAME (nhập từ bàn phím), msg
        except Exception as e:
            print(e)


def send_msg(msg):
    message = msg.encode(FORMAT)
    client.send(message)



if __name__ == "__main__":
    app = QApplication([])
    ui = UI()
    app.exec()