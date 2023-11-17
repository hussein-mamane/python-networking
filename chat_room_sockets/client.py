import threading
import socket


HOST = "127.0.0.1"
PORT = 3500
MAX_RECV_SIZE = 1024

alias = input("Choose an alias (max:15 characters):\n")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def client_receive():
    print('In the receive\n')
    while True:
        try:
            msg = client.recv(MAX_RECV_SIZE).decode('utf-8')
            if msg == "Choose alias":
                client.send(alias.encode('utf-8'))
            else:
                print(msg)
        except:
            print("Client receive error\n")
            client.close()
            break


def client_send():
    print('In the send\n')
    msg = None
    while True:
        msg = input("Type your message:\n")
        message = f"{alias} : {msg}".encode('utf-8')
        client.send(message)


threading.Thread(target=client_receive).start()
threading.Thread(target=client_send).start()
