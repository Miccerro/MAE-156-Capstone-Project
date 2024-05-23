#Atempt to Connect to PLC 
import socket

# PLC IP address and port
PLC_IP = "192.168.1.177"  #PLC's IP address (CAN BE CHANGED AS NEEDED)
PLC_PORT = 8888  # Port number of the PLC server 

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Same syntax, all that needs to be changed is the IP and Port
print("Called successfully")
try:
    # Connect to the PLC server
    client_socket.connect((PLC_IP, PLC_PORT))
    print("Connected to PLC successfully")

except Exception as e:
    print("Error:", e)

finally:
    # Close the socket
    client_socket.close()