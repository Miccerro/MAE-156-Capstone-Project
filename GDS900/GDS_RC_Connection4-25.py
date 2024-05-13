#networking to the GDS:
#Assume that the PC (where this code will be executed) is our Client
import socket
import threading
import xml.etree.ElementTree as ET
import time

#Define constants
DESTINATION_IP = '10.10.10.2' #IP address of PLC
DESTINATION_PORT = 12345
ENCODER = "utf-16" #NOTE: Normally this is utf-8, they are different character encoding schemes (just keep consistant)
BYTESIZE = 1024

def GDS_Connect(): #This function does not recieve message from CornerStone, it only connects
    #Cretea a clientside IPv4 socekt (AF_INET) and TCP (SOCK_STREAM) //Just specifies what to use
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect( (socket.gethostbyname(DESTINATION_IP), DESTINATION_PORT) ) #sent socket to specific location
    #client will wait and listine here //NOTE: IP address will have to be changed to connect to GDS900 (if not already)
    #print("Executed Connection Code")

    #Will have to determine when to close the socket some other time, likely when the analysis is all complete.

    return client_socket


def Heartbeat():
        hb_message = '<Heartbeat/>'
        client_socket.send(hb_message.encode(ENCODER))

        #REPLY SHOULD LOOK LIKE: <Heartbeat ErrorCode=”0” ErrorMessage=”Success”/>


#Asking CAHTGPT:
#The data starts with a 4-byte prefix, telling the length of the data (in bytes)
#Remnaining bytes represnetn the actual data


def GDS_reply():
    buffer = b''  # Used to accumulate data from the GDS

    while True:  # Infinite loop, until broken
        print("before data")
        data = client_socket.recv(1024)  # Receive data // INCREASE BUFFER SIZE?
        print("after data") #WHEN WE TESTED IT, WE DID NOT GET PAST THIS LINE

        if not data:
            break  # break loop if no more data to be read

        buffer += data  # appends data over the many loops (if needed)

        if len(buffer) >= 4:  # if more than the 4bytes (prefix) has been recieved
            # Extract the length of the message from the first 4 bytes (assuming big endian encoding)
            #NOTE: The first 4 bytes contain the message length
            message_length = int.from_bytes(buffer[:4], byteorder='big') #Assume big-endian format NOTE: CAHNGE WAHT HAPPENS
            print("message length:", message_length)
            print(buffer)
            # Check if the entire message has been received
            if len(buffer) >= message_length + 4: #Enter loop if completed reading message
                # Extract the message content
                message = buffer[4:message_length + 4]

                # Process the message here (e.g., print it)
                print("Received message:", message.decode('utf-16'))

                # Remove the processed message from the buffer
                buffer = buffer[message_length + 4:] #Kepp the remaining data that has not been processed YET

