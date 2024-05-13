#Chat Client Side

import socket

#Define constants
#DESTINATION_IP = socket.gethostbyname(socket.gethostname())
DESTINATION_IP = '192.168.1.100'
DESTINATION_PORT = 5000
ENCODER = "utf-8"
BYTESIZE = 1024

#Create client socket and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DESTINATION_IP, DESTINATION_PORT))

#Send/Recieve messages from server
while True:
    #Recieve information from the server
    message = client_socket.recv(BYTESIZE).decode(ENCODER)

    #Quit if the connected server wants to quit, else keep sending messages
    if message == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("\nEnding the Chat (Client Side)... Goodbye!!")
        break
    else:
        print(f"\n{message}")
        message = input("Message: ")
        client_socket.send(message.encode(ENCODER))

#Close Client Socket
client_socket.close()
