import socket
import threading

# Defining host and port to make connection
host = socket.gethostname()
port = 8023

# Defining the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# List of the clients and their nicknames
clients = []
nicknames = []

# broadcasting a message to all the clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling messages from clients
def handle_msg_client(client):
    while True:
        try:
            # Broadcasting the message to everyone
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening function
def receive():
    while True:
        # Accept connection
        client, address = server.accept()
        print("connected with {}".format(str(address)))

        # Request and store Nickname
        client.send("Nick".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print and broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server'.encode('ascii'))

        # Start handling thread for client
        thread = threading.Thread(target=handle_msg_client, args=(client,))
        thread.start()


receive()

