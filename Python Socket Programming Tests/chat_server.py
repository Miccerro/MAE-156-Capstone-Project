#Chat Server Side

import socket

# Define constants
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
ENCODER = "utf-8"
BYTESIZE = 1024

#Create server socket, bind it to ip/port, and listen
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

#Accept any incoming connection and let them know they are connected
print(f"Micah Laptop IP address:{HOST_IP}")
print(f"Server Port Number:{HOST_PORT}")
print("Server is running... \n")
client_socket, client_address = server_socket.accept()
client_socket.send("You are connected to the server...\n".encode(ENCODER))

#Infinite loop to Send/Recieve messages as server
while True:
    #Recieve information from the client
    message = client_socket.recv(BYTESIZE).decode(ENCODER)

    #Quit if client socket wants to quit, else display the message
    if message == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("\n Ending the chat (Server side)... Goodbye!!")
        break
    else:
        print(f"\n{message}")
        message = input("Message: ")
        client_socket.send(message.encode(ENCODER))

# Close the socket
server_socket.close()








