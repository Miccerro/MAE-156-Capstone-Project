import socket

# Define constants
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 6045
ENCODER = "utf-8"
BYTESIZE = 1024

# Define state classes
class State:
    def __init__(self, context):
        self.context = context

    def handle(self, data):
        raise NotImplementedError("Handle method not implemented")

class IdleState(State):
    def handle(self, data):
        if data == "Calibration Mode: ON":
            print("Switching to Calibration State")
            self.context.state = self.context.calibration_state
        elif data == "Analyze Mode: ON":
            print("Switching to Analyze State")
            self.context.state = self.context.analyze_state
        else:
            print("Idle State: No action needed")

class CalibrationState(State):
    def handle(self, data):
        if data == "Calibration Mode: OFF":
            print("Ending Calibration. Switching to Idle State")
            self.context.state = self.context.idle_state
        else:
            print("Calibrating...")

class AnalyzeState(State):
    def handle(self, data):
        if data == "Analyze Mode: OFF":
            print("Ending Analysis. Switching to Idle State")
            self.context.state = self.context.idle_state
        elif data == "Return to Idle":   # SEND THIS STRING FROM PLC WHEN ANALYZE PROCESS FINISHED 
            print("Returning to Idle State from Analyze State")
            self.context.state = self.context.idle_state
        else:
            print("Analyzing...")

# Define the main server context that maintains the state
class ServerContext:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST_IP, HOST_PORT))
        self.server_socket.listen()
        self.client_socket, self.client_address = self.server_socket.accept()
        self.client_socket.send("You are connected to the server...\n".encode(ENCODER))
        
        self.idle_state = IdleState(self)
        self.calibration_state = CalibrationState(self)
        self.analyze_state = AnalyzeState(self)
        self.state = self.idle_state  # Default state is Idle

    def run(self):
        try:
            while True:
                message = self.client_socket.recv(BYTESIZE).decode(ENCODER)
                if message == "quit":
                    self.client_socket.send("quit".encode(ENCODER))
                    print("\nEnding the chat (Server side)... Goodbye!!")
                    break
                else:
                    self.state.handle(message)
        finally:
            self.server_socket.close()

# Create server context and run it
server_context = ServerContext()
server_context.run()


# import socket

# # Define constants
# HOST_IP = socket.gethostbyname(socket.gethostname())
# HOST_PORT = 6045
# ENCODER = "utf-8"
# BYTESIZE = 1024

# #Create server socket, bind it to ip/port, and listen
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((HOST_IP, HOST_PORT))
# server_socket.listen()

# #Accept any incoming connection and let them know they are connected
# client_socket, client_address = server_socket.accept()
# client_socket.send("You are connected to the server...\n".encode(ENCODER))

# #Infinite loop to Recieve messages as server
# while True:
#     #Recieve information from the client
#     message = client_socket.recv(BYTESIZE).decode(ENCODER)

#     #Quit if client socket wants to quit, else display the message
#     if message == "quit":
#         client_socket.send("quit".encode(ENCODER))
#         print("\n Ending the chat (Server side)... Goodbye!!")
#         break
#     else:
#         print(f"\n{message}")

# # Close the socket
# server_socket.close()