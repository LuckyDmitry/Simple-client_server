import socket
import threading
import time

encoding = 'utf-8'


server_socket = socket.socket()
server_socket.bind((socket.gethostname(), 9090))
server_socket.listen(3)

all_clients = []
print("Server is working")


def main_handle(client_socket, client_address):
    client_socket.send(bytes("Hello!", encoding))
    client_name = str(client_socket.recv(30), encoding)
    while True:
        try:
            message = str(client_socket.recv(1024), encoding)
            if message:
                print(f"{client_name} >> {message}")
                if client_socket not in all_clients:
                    all_clients.append(client_socket)
                message_handle(client_socket, message, client_name)
            else:
                remove_client(client_socket)
        except:
            continue


def message_handle(client_socket, message, client_name):
    for client in all_clients:
        if client_socket != client:
            current_time = time.strftime("%H.%M", time.localtime())
            client.send(bytes(f"[{current_time}] -- {client_name} -- {message}", encoding))


def remove_client(client_socket):
    if client_socket in all_clients:
        all_clients.remove(client_socket)


def close_clients():
    for client in all_clients:
        client.close()
        all_clients.remove(client)


while True:
    try:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=main_handle, args=(client_socket, client_address))
        client_thread.start()
    except:
        print("\nServer stopped")
        close_clients()
        break
        
server_socket.close()
