import threading
import socket

HOST = "127.0.0.1"
PORT = 3500
MAX_RECV_SIZE = 1024
ALIAS_MAX_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
aliases = []


def broadcast(msg):
    for client in clients:
        client.send(msg)


def handle_client(client):
    while True:
        try:
            msg = client.recv(MAX_RECV_SIZE)
            broadcast(msg)
        except:
            index = clients.index(client)
            client.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f"{alias} has left !\n".encode('utf-8'))
            aliases.remove(alias)
            break


def run_server():
    print(f'[LISTENING], port:{PORT}')
    while True:
        client, addr = server.accept()
        print(f"Connected to client {str(addr)}")
        client.send("Choose alias".encode('utf-8'))
        alias = client.recv(ALIAS_MAX_SIZE)
        aliases.append(alias)
        clients.append(client)
        broadcast(f'alias {alias} joined the room\n'.encode('utf-8'))
        client.send('You are connected\n'.encode('utf-8'))
        threading.Thread(target=handle_client, args=(client,)).start()


if __name__ == '__main__':
    run_server()
