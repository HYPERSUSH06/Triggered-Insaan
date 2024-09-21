import socket
import time
import threading
import keyboard

def signal_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 65432))
    sock.listen(1)

    time.sleep(0.1)

    conn, addr = sock.accept()
    print(f"Connected to {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            key = data.decode()
            if len(key) == 1 and key.isalnum():
                keyboard.send(key)
            time.sleep(0.001)

if __name__ == "__main__":
    signal_server()
