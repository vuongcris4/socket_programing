import socket
import threading

HEADER = 64
PORT = 8000
SERVER = ""
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!exit"
clients = {} # {conn: "Name client"}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send_client_quit(conn):
    msg_disconnected = f'[SERVER]: Client "{clients[conn]}" is quitted' # Tên client vừa thoát
    print(msg_disconnected)
    del clients[conn]

    for each_conn in clients.keys():                  # Thông báo tới các client còn lại client này đã quit
        each_conn.send(msg_disconnected.encode(FORMAT))


def handle_client(conn, addr):
    # print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            try:
                msg = conn.recv(HEADER).decode(FORMAT)   
                print(msg)
            except ConnectionResetError:
                send_client_quit(conn)
                break


            # Khi terminate cmd phía client hoặc gõ !exit
            if not msg or DISCONNECT_MESSAGE in msg:       
                send_client_quit(conn)
                break                                 
            
            for each_conn in clients.keys():
                if each_conn != conn:
                    try:
                        each_conn.send(msg.encode(FORMAT))  # Send message tới tất cả các client còn đang kết nối
                    except OSError as e:
                        print(f"[ERROR] Client Socket was closed {each_conn}: {e}") # Đề phòng lỗi
                        del clients[conn]

    except ConnectionAbortedError: # Socket lỗi tự đóng
        print(f"[CONNECTION LOST] {addr} disconnected unexpectedly")
        del clients[conn]

    conn.close()



def start():
    server.listen()
    print(f"[LISTENING] Server is listening on")
    while True:
        conn, addr = server.accept()
        clients.update({conn: conn.recv(HEADER).decode(FORMAT)}) # Nhận conn, tên client
        conn.send("!OK!".encode(FORMAT)) # Gửi tín hiệu báo client kết nối thành công

        # Thông báo các client còn lại khi new client join
        msg_connect = f'[SERVER]: Client "{clients[conn]}" is joined'
        print(msg_connect)
        for each_conn in clients.keys():    
            if conn != each_conn: 
                try:           
                    each_conn.send(msg_connect.encode(FORMAT))
                except OSError:
                    msg_disconnected = f'[SERVER]: Client "{clients[conn]}" is quitted' # Tên client vừa thoát
                    print(msg_disconnected)
                    break

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start()