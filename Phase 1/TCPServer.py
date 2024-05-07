import socket
import threading

HEADER = 1024
PORT = 8003
FORMAT = "UTF-8"
SERVER = "localhost"
ADDR = (SERVER, PORT)
clients = {}  # {conn: "Name client"}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send_client_quit(conn):
    # Tên client vừa thoát
    msg_disconnected = f'[SERVER]: Client "{clients[conn]}" is quitted'
    print(msg_disconnected)
    del clients[conn]
    # Thông báo tới các client còn lại client này đã quit
    for each_conn in clients.keys():
        each_conn.send(msg_disconnected.encode(FORMAT))


def handle_client(conn, addr):
    while True:
        # Nhận message
        msg = conn.recv(HEADER).decode(FORMAT)
        print(msg)


        # Send message tới tất cả các client còn đang kết nối
        for each_conn in clients.keys():
            if each_conn != conn:
                each_conn.send(msg.encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on")
    while True:
        conn, addr = server.accept()
        NAME = conn.recv(HEADER).decode(FORMAT)  # Phía client gửi name đầu tiên
        clients.update({conn: NAME})  # Nhận conn, tên client

        # Thông báo các client còn lại khi new client join
        msg_connect = f'[SERVER]: Client "{clients[conn]}" is joined'
        print(msg_connect)
        for each_conn in clients.keys():
            if conn != each_conn:
                each_conn.send(msg_connect.encode(FORMAT))

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start()
