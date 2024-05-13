# TCP Server Side
import socket
# Get IP Address of host Dynamically
print(socket.gethostname())  #hostname
print(socket.gethostbyname(socket.gethostname())) #ip of the given hostname
#ip_address = ("123.144.199.10",12224)
port_num = 12224

# Create a server side socket using IPV4 (AF_INET) and TCP (SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind our new socket to a tuple (IP Address, Port Address)
server_socket.bind((socket.gethostbyname(socket.gethostname()),port_num))

#Put socket into listening mode to listen for any possible connections
server_socket.listen()

#Listen forever to accept ANY connection

while True:
    # Accept every single connection and store two pieces of information
    client_socket, client_address = server_socket.accept()
    print(type(client_socket))
    print(client_socket)
    print(type(client_address))
    print(client_address)

    print(f"Connected to {client_address}\n")


    #Send a message to client that just connected
    # NOTE: Message has to be encoded and send as bytes object, can't 
    # just send strings 
    
    client_socket.send("You are Connected!!!!".encode("utf-8")) 

    # close connection
    server_socket.close()
    break