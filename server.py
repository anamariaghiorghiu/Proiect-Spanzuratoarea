import socket
import sys


# GET THE HOST AND PORT
host = input('Enter the host:')
port = int(input('Enter the port:'))

# CREATE THE SOCKET
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Server running on Host ' + host + '| Port ' + str(port))

# CONNECT THE SOCKET TO THE HOST AND PORT, LISTEN TO CLIENT
my_socket.bind((host, port))
my_socket.listen(6)

number_of_clients = 0
word_to_guess = ''
clients_sockets = []
clients_addresses = []


def connection():
    global number_of_clients
    print("Game will start once two players connect.")

    while True:
        client_socket, client_address = my_socket.accept()
        number_of_clients += 1
        clients_sockets.append(client_socket)
        clients_addresses.append(client_address)
        print("New player is here.")
        send_message(client_socket, 'Connected successfully.')
        print("New connection with ID: " + str(number_of_clients) + " at current address: " + str(client_address))
        if number_of_clients == 2:
            start()


def send_message(client_socket, message):
    client_socket.send(message.encode('utf-8'))


def start():
    number_of_tries = 0
    print('GAME STARTS IN 3..2..1..go!')

    # GET DEFINITION FROM FIRST CLIENT
    definition = clients_sockets[0].recv(1024).decode('utf-8')
    print('Definition given by client: ' + definition)
    send_message(clients_sockets[1], definition)

    # ASSIGNING ROLES
    send_message(clients_sockets[0], 'Please enter a word.')
    send_message(clients_sockets[1], 'You will now guess the word!')

    # GET MESSAGE FROM FIRST CLIENT
    word = clients_sockets[0].recv(1024).decode('utf-8')
    print('The word given by client: ' + word)

    # SENDING CENSORED WORD TO THE OTHER CLIENT
    censored_word = ""
    for i in range(0, len(word)):
        censored_word += "_"
    send_message(clients_sockets[1], censored_word)

    # HANGMAN ALGORITHM
    max_nr_of_tries = len(word)  # condition
    game_is_not_over = True
    letters = [x for x in word]
    # SEARCH
    while game_is_not_over:
        letter = clients_sockets[1].recv(1024).decode('utf-8')
        if letter not in word:
            number_of_tries = number_of_tries + 1
        nr = max_nr_of_tries - number_of_tries
        send_message(clients_sockets[1], str(nr))
        if number_of_tries == max_nr_of_tries - 1:
            for client_socket in clients_sockets:
                send_message(client_socket, 'Game over.')
            sys.exit()
        for i in range(0, len(letters)):
            if letter == letters[i]:
                censored_word_split = [x for x in censored_word]
                censored_word_split[i] = letters[i]
                censored_word = ''.join(censored_word_split)
                if censored_word == word:
                    for client_socket in clients_sockets:
                        send_message(client_socket, 'Game over.')
                    sys.exit()
        print('The client tried to guess wrong ' + str(number_of_tries) + ' times')
        send_message(clients_sockets[1], censored_word)


if __name__ == '__main__':
    connection()
