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
    message = client_socket.recv(1024).decode('utf-8')
    new_message = client_socket.recv(1024).decode('utf-8')
    print(new_message)
    #INITIAL MESSAGE
    print(message)
    # CENSORED WORD
    message = client_socket.recv(1024).decode('utf-8')
    print(message)

    while connection_is_going:
        input_letter = input("Enter a letter: ")
        if input_letter.isalpha() and len(input_letter) == 1:
            result_from_parsing = (input_letter, True)
        else:
            result_from_parsing = (input_letter, False)
        if result_from_parsing[1]:
            letter = result_from_parsing[0]
        else:
            # ONLY THE FIRST LETTER
            letter = result_from_parsing[0][0]
        send_message(client_socket, letter)

        nr_of_tries = client_socket.recv(1024).decode('utf-8')
        print(nr_of_tries)

        # RECEIVE THE CENSORED WORD AFTER GUESSING
        message = client_socket.recv(1024).decode('utf-8')
        print(message)
        if message == 'Game over.':
            sys.exit()


if __name__ == '__main__':
    connection()