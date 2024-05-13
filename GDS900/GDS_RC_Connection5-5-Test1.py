import socket
import xml.etree.ElementTree as ET

# Define constants
DESTINATION_IP = '10.10.10.2'  # IP address of PLC
DESTINATION_PORT = 12345
ENCODER = "utf-16"  # Character encoding scheme
BYTESIZE = 1024

def GDS_Connect():
    """
    Establishes a connection to the GDS and returns the socket.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((socket.gethostbyname(DESTINATION_IP), DESTINATION_PORT))

    print("Client_Socket in GDS_COnnect:", client_socket)
    return client_socket




# def Heartbeat1(client_socket):
#     """
#     Sends a heartbeat message to the server and receives the response.
#     """
#     print("Client_Socket in GDS_COnnect:", client_socket)

#     hb_message = '<Heartbeat/>'
#     client_socket.send(hb_message.encode(ENCODER))
    
#     # Receive response from the server
#     response = client_socket.recv(BYTESIZE).decode(ENCODER)
#     print("Server response:", response)

def Heartbeat2(client_socket):
    """
    Sends a heartbeat message to the server and receives the response.
    """
    print("Client_Socket in GDS_COnnect:", client_socket)

    hb_message = '<Heartbeat/>'
    client_socket.send(hb_message.encode(ENCODER))
    
    # Receive response from the server
    response = client_socket.recv(BYTESIZE).decode(ENCODER)
    print("Server response:", response)


################################
client_socket = GDS_Connect()
input("Press Enter to continue. Connect Complete, Heartbeat next")
Heartbeat2(client_socket)
input("Press Enter to continue. Connect Complete, Heartbeat next")
