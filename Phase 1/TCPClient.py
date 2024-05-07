import socket
import threading

HEADER = 1024
PORT = 8003
FORMAT = "UTF-8"
SERVER = "localhost"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4, TCP
client.connect(ADDR)
connected = True

NAME = input("Nhập tên của bạn: ")
client.send(NAME.encode(FORMAT))


def handle_rev(client):
    global connected
    while connected:
        msg = client.recv(HEADER).decode(FORMAT)
        print(msg)


def handle_send(client):
    global connected
    while connected:
        msg = input(f"[{NAME}]: ")
        send_msg(f"[{NAME}]: {msg}")  # SEND NAME (nhập từ bàn phím), msg



def send_msg(msg):
    message = msg.encode(FORMAT)
    client.send(message)


thread = threading.Thread(target=handle_rev, args=(client,))
thread.start()
thread = threading.Thread(target=handle_send, args=(client,))
thread.start()
