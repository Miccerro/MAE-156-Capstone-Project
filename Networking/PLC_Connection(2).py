import socket
import struct

ENCODER = 'utf-8'

def sendMessage(message, client_socket):
    print("Send Message:", message)
    encoded = message.encode(ENCODER)
    length = len(encoded)
    packed = struct.pack('<I', length)  # Packs the length of the encoded message into binary format

    # Send data length
    client_socket.send(packed)
    # Send encoded data
    client_socket.send(encoded)

    # Read response length
    responseLengthBytes = b''
    while len(responseLengthBytes) < 4:
        more = client_socket.recv(4 - len(responseLengthBytes))
        if not more:
            raise Exception("Socket connection broken")
        responseLengthBytes += more

    responseLength = struct.unpack('<I', responseLengthBytes)[0]  # Unpacks received bytes back into integer
    print("Message Response Length:", responseLength)
    
    # Read response data
    response = b''
    while len(response) < responseLength:
        more = client_socket.recv(responseLength - len(response))
        if not more:
            raise Exception("Socket connection broken")
        response += more

    print("Message Response:", response.decode(ENCODER))
    return response.decode(ENCODER)

def main():
    # Server's IP address and port number to match the Arduino configuration
    server_ip = '192.168.1.177'
    server_port = 8888

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print("Connected to server at {}:{}".format(server_ip, server_port))

        while True:
            # Get user input
            message = input("Enter message to send (or 'exit' to quit): ")
            if message.lower() == 'exit':
                sendMessage(message, client_socket)
                break

            # Send and receive message
            response = sendMessage(message, client_socket)

    finally:
        # Close the connection
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
