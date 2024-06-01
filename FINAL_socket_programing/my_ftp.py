import ftplib
import os

# ĐĂNG NHẬP FTP SERVER
FTP_HOST = "ftp.dlptest.com"
FTP_USER = "dlpuser"
FTP_PASS = "rNrKYTX9g7z3RgJRmxWuGHbeu"

def send_file(full_path):
    result_upload_file = ""
    file_name = os.path.basename(full_path) # Lấy tên file từ đường dẫn đầy đủ
    try:
        ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)  # connect to FTP Server
        ftp.encoding = "utf-8"
        with open(full_path, "rb") as file:
            result_upload_file = ftp.storbinary(f"STOR {file_name}", file)  # UPLOAD file lên FTP Server
        ftp.quit()
    except Exception as e:
        return e

    if result_upload_file == "226 Transfer complete.":
        return "Gửi file thành công"
    return "Gửi file thất bại"


def receive_file(local_name, file_name):
    result_receive_file = ""
    try:
        ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)  # connect to FTP Server
        ftp.encoding = "utf-8"
        with open(f"ReceivedFile/{local_name}", "wb") as file:  # Lưu file vào folder ReceivedFile với tên {local_name}
            result_receive_file = ftp.retrbinary(f"RETR {file_name}", file.write)   # Lấy {file_name} từ FTP Server
        ftp.quit()
    except Exception as e:
        return e

    if result_receive_file == "226 Transfer complete.":
        return "Gửi file thành công"
    return "Gửi file thất bại"
