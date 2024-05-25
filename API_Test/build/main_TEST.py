import socket
import time
import threading
#import cornerstone_commands

# Define constants
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 6045
ENCODER = "utf-8"
BYTESIZE = 1024

# Default Variables
Wagon_Wheel = 8

# Define function to handle PLC connection
def handle_plc_connection():
    print("Connecting to PLC...")
    time.sleep(2)
    print("PLC connection established")
    # Add your actual PLC connection code here
    return "PLC Connected"  # Return message indicating success

# Define function to handle Cornerstone connection
def handle_cornerstone_connection():
    print("Connecting to Cornerstone...")
    time.sleep(2)
    print("Cornerstone connection established")
    # Add your actual Cornerstone connection code here
    return "Cornerstone Connected"  # Return message indicating success

# Define State Classes
class State:
    def __init__(self, context,client_socket):
        self.context = context
        self.client_socket = client_socket  # Store the client_socket in each state

    def handle(self, data):
        raise NotImplementedError("Each state must implement a handle method.")

class IdleState(State):
    def handle(self, data): # Different commands that will execute when specific commands are sent to server instance while code in idle state
        #Handles commands specific to idle state
        print(f"Idle State: Received {data}")
        if data == "calibration on": 
            self.context.change_state('calibration')
        if data == "Start Analysis Process": 
            self.context.change_state('analysis')
        elif data == '8-Spoke Wagon Wheel Selected':
            #INSERT FUNCTION TO SEND 8 SPOKE SELECTION TO PLC
            print(data)
        elif data == '16-Spoke Wagon Wheel Selected':
            #INSERT FUNCTION TO SEND 16 SPOKE SELECTION TO PLC
            print(data)
        elif data == "connect plc request":
            # Simulate socket connection operation to PLC then sends confirmation upon connection to gui
            response = handle_plc_connection()
            self.client_socket.send(response.encode(ENCODER))
        elif data == "connect cornerstone request":
            # Simulate socket connection operation to Cornerstone then sends confirmation upon connection to gui
            response = handle_cornerstone_connection()
            self.client_socket.send(response.encode(ENCODER))

class CalibrationState(State):
    def __init__(self, context, client_socket):
        super().__init__(context, client_socket)
        self.initialized = False  # To track if the initial processes have been run
        self.start_calibration_process()

    def handle(self, data):
        if data == "calibration off":
            self.client_socket.send("Calibration Mode: OFF".encode(ENCODER)) #send gui message that automatically turns buttons to off state
            self.context.change_state('idle')

    def start_calibration_process(self):
        print("Calibration: Starting")
        self.client_socket.send("Calibration Mode: ON".encode(ENCODER))
        #INSERT FUNCTION TO SEND TO PLC THAT CALIBRATION MODE IS ON 

class AnalysisState(State):
    def __init__(self, context):
        super().__init__(context)
        self.sub_states = {
            'initializing': InitializingState(self.context),
            'loading': LoadingState(self.context),
            'analyzing': SampleAnalysisState(self.context)
        }
        self.current_sub_state = self.sub_states['initializing']
        self.is_active = False  # Indicates if the analysis process is active

    def enter_state(self):
        # Actions to execute when entering the analysis state
        print("Entering Analysis State: Starting analysis processes...")
        self.start_analysis_processes()
        self.is_active = True

    def start_analysis_processes(self):
        # Define the series of processes to start
        print("Starting initialization of analysis process")
        #INSERT STARTING ANALYSIS PROCESSES

    def handle(self, data): #This is where you put what will occur when a certain message is sent to server when code is in this current state
        #Handles commands specific to analysis state
        print(f"Analysis State: Received {data}")
        if 'move to' in data:
            self.change_sub_state(data.split()[-1])
        else:
            self.current_sub_state.handle(data)

        # Code to handle when gui sends over specific analysis state command again and is already in analysis state    
        if data == "Start Analysis Process":
            if not self.is_active:
                self.start_analysis_processes()
            else:
                print("Analysis is already running.")
        elif data == "stop":
            print("Stopping analysis processes...")
            self.context.change_state('idle')  # Optionally switch to idle state
            self.is_active = False

    def change_sub_state(self, sub_state_key):
        if sub_state_key in self.sub_states:
            self.current_sub_state = self.sub_states[sub_state_key]
            print(f"Analysis State: Transitioned to {sub_state_key} sub-state.")

class InitializingState(State):
    def handle(self, data):
        print(f"Initializing State: Handling {data}")

class LoadingState(State):
    def handle(self, data):
        print(f"Loading State: Handling {data}")

class SampleAnalysisState(State):
    def handle(self, data):
        print(f"Sample Analysis State: Handling {data}")

# Context class that manages states
class Context:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.states = {  # each 'state' is like key that switches states based on it
            'idle': IdleState(self),
            'analysis': AnalysisState(self),
            'calibration': CalibrationState(self)
        }
        self.state = self.states['idle']

    def change_state(self, state_name):
        self.state = self.states[state_name]
        print(f"Context: Transitioned to {state_name} state.")
        self.state.enter_state()  # Call enter_state of the new state

    def handle(self, data):
        self.state.handle(data)

# Main server code
class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST_IP, HOST_PORT))
        self.server_socket.listen()

    def run(self):
        print("Server is running...")
        client_socket, client_address = self.server_socket.accept()
        print(f"Connected to {client_address}")
        context = Context(client_socket)  # Pass the client_socket to the context instance

        try:
            while True:
                data = client_socket.recv(BYTESIZE).decode(ENCODER)
                if data == 'quit':
                    print("Server stopping...")
                    break
                else:
                    self.context.handle(data)
        finally:
            client_socket.close()
            self.server_socket.close()

if __name__ == "__main__":
    server = Server()
    server.run()

# # Define function to handle PLC connection
# def handle_plc_connection():
#     print("Connecting to PLC...")
#     time.sleep(2)
#     print("PLC connection established")
#     # Add your actual PLC connection code here
#     return "PLC Connected"  # Return message indicating success

# # Define function to handle Cornerstone connection
# def handle_cornerstone_connection():
#     print("Connecting to Cornerstone...")
#     time.sleep(2)
#     print("Cornerstone connection established")
#     # Add your actual Cornerstone connection code here
#     return "Cornerstone Connected"  # Return message indicating success

# # Define State Classes
# class State:
#     def __init__(self, context):
#         self.context = context

#     def handle(self, data):
#         raise NotImplementedError("Handle method not implemented.")

# class IdleState(State):
#     def handle(self, data):
#         if data == "Connect to PLC":
#             self.context.plc.connect()
#         elif data == "Connect to CornerStone":
#             self.context.cornerstone.connect()
#         # Additional handlers for idle state

# class CalibrationState(State):
#     def handle(self, data):
#         # Handle calibration mode activation, adjustments, etc.
#         pass

# class AnalysisState(State):
#     def handle(self, data):
#         if data == "Start Analysis Process":
#             print("Analysis state activated. Beginning XML commands execution.")
#             self.run_xml_commands()

#     def run_xml_commands(self):
#         # Placeholder for the series of functions that send XML commands
#         print("Sending XML command 1...")
#         # simulate sending XML command
#         print("Sending XML command 2...")
#         # simulate sending another XML command
#         # Add more as needed


# # Nested states for analysis
# class InitializingState(State):
#     def handle(self, data):
#         # Send XML to Cornerstone to initialize sample count
#         pass

# class LoadingState(State):
#     def handle(self, data):
#         # Logic to handle loading including error checking
#         pass

# class SampleAnalysisState(State):
#     def handle(self, data):
#         # Handle sample analysis
#         pass
    
# # More nested states as needed...
# class ServerContext:
#     def __init__(self):
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server_socket.bind((HOST_IP, HOST_PORT))
#         self.server_socket.listen()
#         self.client_socket, self.client_address = self.server_socket.accept()
#         self.client_socket.send("You are connected to the server...\n".encode(ENCODER))

#         self.states = {
#             'idle': IdleState(self),
#             'calibration': CalibrationState(self),
#             'analysis': AnalysisState(self)
#         }
#         self.state = self.states['idle']  # Start in idle state

#     def switch_state(self, state_key):
#         if state_key in self.states:
#             self.state = self.states[state_key]
#             print(f"Switched to {state_key} state.")


#     def run(self):
#         try:
#             while True:
#                 message = self.client_socket.recv(BYTESIZE).decode(ENCODER)
#                 if message == '8-Spoke Wagon Wheel Selected':
#                     #INSERT FUNCTION TO SEND 8 SPOKE SELECTION TO PLC
#                     print(message)
#                 elif message == '16-Spoke Wagon Wheel Selected':
#                     #INSERT FUNCTION TO SEND 16 SPOKE SELECTION TO PLC
#                     print(message)
#                 elif message == 'calibration on':
#                     self.switch_state('calibration')
#                     print(message)
#                     #sends string that overrides manual button press causing ON state
#                     self.client_socket.send("Calibration Mode: ON".encode(ENCODER))
#                     #INSERT FUNCTION TO SEND CALIBRATION MODE ON TO PLC
#                     # When finished with calibrating use: self.client_socket.send("Calibration Mode: OFF".encode(ENCODER))
#                     # to send gui message that automatically turns buttons to off state                      
#                 elif message == 'calibration off':
#                     self.switch_state('idle')
#                     print(message)
#                      #sends string that overrides manual button press causing OFF state
#                     self.client_socket.send("Calibration Mode: OFF".encode(ENCODER))
#                     #INSERT FUNCTION TO SEND CALIBRATION MODE OFF TO PLC 
#                 elif message == "connect plc request":
#                     # Simulate socket connection operation to PLC then sends confirmation upon connection to gui
#                     response = handle_plc_connection()
#                     self.client_socket.send(response.encode(ENCODER))
#                 elif message == "connect cornerstone request":
#                     # Simulate socket connection operation to Cornerstone then sends confirmation upon connection to gui
#                     response = handle_cornerstone_connection()
#                     self.client_socket.send(response.encode(ENCODER))
#                 elif message == 'quit':
#                     self.client_socket.send("quit".encode(ENCODER))
#                     print("Server stopping...")
#                     break
#                 else:
#                     self.client_socket.recv(BYTESIZE).decode(ENCODER)
#                     self.state.handle(message)
#         finally:
#             self.client_socket.close()
#             self.server_socket.close()


# if __name__ == "__main__":
#     context = ServerContext()
#     context.run()

#### GUI Tests ####

