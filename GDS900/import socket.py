import socket
import xml.etree.ElementTree as ET
import threading
import time

# Define constants
DESTINATION_IP = '10.10.10.2'  # IP address of PLC
DESTINATION_PORT = 12345
ENCODER = "utf-16"  # Character encoding scheme
BYTESIZE = 1024
HEARTBEAT_INTERVAL = 30  # Interval in seconds between heartbeat messages

def GDS_Connect():
    """
    Establishes a connection to the GDS and returns the socket.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((socket.gethostbyname(DESTINATION_IP), DESTINATION_PORT))
    print("Client_Socket in GDS_Connect:", client_socket)
    return client_socket

def Heartbeat(client_socket):
    """
    Sends a heartbeat message to the server and receives the response.
    """
    print("Client_Socket in Heartbeat:", client_socket)
    hb_message = '<Heartbeat/>'
    client_socket.send(hb_message.encode(ENCODER))
    
    # Receive response from the server
    response = client_socket.recv(BYTESIZE).decode(ENCODER)
    print("Server response:", response)

def send_heartbeat(client_socket):
    """
    Sends a heartbeat message to the server at regular intervals.
    """
    while True:
        Heartbeat(client_socket)
        time.sleep(HEARTBEAT_INTERVAL)

# Main program
if __name__ == "__main__":
    # Establish connection to GDS
    client_socket = GDS_Connect()
    
    # Start a separate thread to send heartbeat messages
    heartbeat_thread = threading.Thread(target=send_heartbeat, args=(client_socket,))
    heartbeat_thread.daemon = True
    heartbeat_thread.start()

