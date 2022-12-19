import socket
import sys

# GET THE HOST AND PORT
host = input('Enter the host:')
port = int(input('Enter the port:'))

# CREATE SOCKET
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connection_is_going = True


def connection():
    client_socket.connect((host, port))
    while connection_is_going:
        print(client_socket.recv(1024).decode('utf-8'))
        start()
        break


def send_message(client_socket, message):
    client_socket.send(message.encode('utf-8'))


def start():
    definition = input("DEFINITION: ")
    send_message(client_socket, definition)

    message = client_socket.recv(1024).decode('utf-8')
    print(message)
    word = input("WORD: ")
    send_message(client_socket, word)
    while connection_is_going:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)
        if message == 'Game over.':
            sys.exit()


if __name__ == '__main__':
    connection()