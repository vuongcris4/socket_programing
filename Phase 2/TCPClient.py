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

NAME = input("Nhập tên của bạn: ")


def handle_rev():
    global connected, client
    while True:
        if connected == False:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4, TCP
                client.connect(ADDR)
                client.send(NAME.encode(FORMAT))
                connected = True
                print(f"Kết nối tới {SERVER} thành công!")

            except ConnectionRefusedError as e:
                print("...Đang cố gắng kết nối tới server....")
                connected = False
                sleep(1)

        if connected == True:
            try:
                msg = client.recv(HEADER).decode(FORMAT)
                if not msg:
                    print("Server đã bị tắt")
                    connected = False 
                print(msg)
                sleep(0.1)
            except Exception:
                print("Server đã bị tắt")
                connected = False
                sleep(1)



def handle_send(client):
    global connected
    while True:
        msg = input(f"[{NAME}]: ")
        send_msg(f"[{NAME}]: {msg}")  # SEND NAME (nhập từ bàn phím), msg



def send_msg(msg):
    message = msg.encode(FORMAT)
    client.send(message)


thread = threading.Thread(target=handle_rev)
thread.start()
thread = threading.Thread(target=handle_send, args=(client,))
thread.start()
