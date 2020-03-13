import socket
import threading
import sys


client_socket = socket.socket()
client_socket.connect((socket.gethostname(), 9090))


def get_message():
    while True:
        try:
            message = str(client_socket.recv(1024), 'utf-8')
            if not message:
                client_socket.close()
            else:
                print(message)
        except:
            continue


def chat_execute():
    while True:
        try:
            message = input()
            if message != "":
                client_socket.send(bytes(message, "utf-8"))
        except:
            try:
                client_socket.send(bytes("User left chat", "utf-8"))
            except:
                print("Server unavailable")
                client_socket.close()
                sys.exit()


def validation_user():
    client_name = input("Enter your name: ")
    client_socket.send(bytes(client_name, 'utf-8'))


def main():
    th = threading.Thread(target=get_message, daemon=True).start()
    validation_user()
    chat_execute()


if __name__ == '__main__':
    main()
