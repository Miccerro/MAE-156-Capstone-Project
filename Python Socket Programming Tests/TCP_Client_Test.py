#TCP Client Side

import socket

port_num = 12224
#Create a client side IPV4 Socket (AF_INET and TCP (SOCK_STREAM))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to a server located at a given IP and Port
client_socket.connect((socket.gethostbyname(socket.gethostname()),port_num))

# Recieve a message from the server ... you must specify the max number of bytes to recieve
message = client_socket.recv(1024)  #1024 is arbitrary number of bites, for a string 1 byte = 1 character
print(type(message))
print(message.decode("utf-8"))

# Close the client socket
client_socket.close()

