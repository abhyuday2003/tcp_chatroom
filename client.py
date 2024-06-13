import socket
import threading

# Defining host and port to make connection
host = socket.gethostname()
port = 8023

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Listenting to server and sending Nickname
def receive():
    while True:
        try:
            # Receive message from server
            # If message is 'Nick' send nickname
            message = client.recv(1024).decode('ascii')

            if message == 'Nick':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close connection when Error
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = "{}: {}".format(nickname, input())
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()