import socket

def main():
    host = 'localhost'  # The server's hostname or IP address
    port = 6049         # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as plc_socket:
        try:
            # Connect to the server
            plc_socket.connect((host, port))
            print("Connected to PLC server.")

            # List of commands to send to the server
            commands = ['8-Spoke Wagon Wheel Selected', '16-Spoke Wagon Wheel Selected', 'Start Analysis Process', 'connect plc']

            # Send commands to the server
            for command in commands:
                print(f"Sending: {command}")
                plc_socket.sendall(command.encode('utf-8'))

                # Receive response from the server
                response = plc_socket.recv(1024).decode('utf-8')
                print(f"Received: {response}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
