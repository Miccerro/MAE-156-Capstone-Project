
import socket
import time

def main():
    # Set the server's host and port
    host = 'localhost'
    port = 6049

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Start listening for clients
    server_socket.listen(1)
    print(f"PLC Simulator Server running on {host}:{port}, Waiting for Connection...")

    try:
        # Accept a connection
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")

        # Handle the client
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received from client: {data}")

            # Respond based on the received data
            if data == '8-Spoke':
                response = "8-Spoke Wagon Wheel Confirmed"
            elif data == '16-Spoke':
                response = "16-Spoke Wagon Wheel Confirmed"
            elif data == 'Start Analysis Process':
                response = "Analysis Started"
            elif data == 'connect plc':
                time.sleep(3)
                response = "PLC Connection Established"
            else:
                response = "Command Not Recognized"

            # Send response to the client
            client_socket.send(response.encode('utf-8'))

    finally:
        # Close the connection
        client_socket.close()
        server_socket.close()
        print("Server stopped.")

if __name__ == "__main__":
    main()
