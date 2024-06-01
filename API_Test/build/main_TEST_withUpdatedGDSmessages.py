import socket
import time
import threading
import struct
import xml.etree.ElementTree as ET
#import cornerstone_commands

# Define constants
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 6045
ENCODER = "utf-8"
BYTESIZE = 1024
PLC_IP = 'localhost' 
PLC_PORT = 6049  
CORNERSTONE_SERVER_IP = 'localhost'
CORNERSTONE_SERVER_PORT = 12345
CORNERSTONE_ENCODER = 'utf-16le'

# Global Variables
wagon_wheel = 8
PLC_socket = None  # Variable to track Arduino connection
CORNERSTONE_socket = None  # Variable to track CornerStone connection

# Cornerstone XML Message variables
Login_Password_XML = '<Logon User="156a" Password="156a156a"/>'
AddSample8Spoke_XML = '''
    <AddSamples Cookie="AddSamples" Culture="en-US">
  <Set>
    <Field Id="SampleType">Sample</Field>
    <Field Id="Name">PyTese2.1</Field>
    <Field Id="Description"></Field>
    <Field Id="MethodKey">0</Field>
    <Field Id="StandardKey">0</Field>
  </Set>
  <Replicates>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke1</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke2</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke3</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke4</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke5</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke6</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke7</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke8</Field>
      <Field Id="Location"></Field>
    </Replicate>
  </Replicates>
</AddSamples>
'''
AddSample16Spoke_XML = '''
    <AddSamples Cookie="AddSamples" Culture="en-US">
  <Set>
    <Field Id="SampleType">Sample</Field>
    <Field Id="Name">PyTese2.1</Field>
    <Field Id="Description"></Field>
    <Field Id="MethodKey">0</Field>
    <Field Id="StandardKey">0</Field>
  </Set>
  <Replicates>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke1</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke2</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke3</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke4</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke5</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke6</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke7</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke8</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke9</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke10</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke11</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke12</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke13</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke14</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke15</Field>
      <Field Id="Location"></Field>
    </Replicate>
    <Replicate>
      <Field Id="Mass">1.0</Field>
      <Field Id="Comments">Spoke16</Field>
      <Field Id="Location"></Field>
    </Replicate>
  </Replicates>
</AddSamples>
'''
LRAS_message = '<LastRemoteAddedSets Cookie="LastRemoteAddedSets" Culture="en-US" />'
DAA_message = '<AutoAnalyze State="DISABLED" />'
LSS1 = '<ExecuteSequence Sequence="Load Sample Step 1" />'
LSS2 = '<ExecuteSequence Sequence="Load Sample Step 2" />'
LSS3 = '<ExecuteSequence Sequence="Load Sample Step 3" />'
SampleLoadState_message = '<StringValue Key="Sample Load State" Cookie="StringValue" Culture="en-US" />'
Analyze_Sample_message = '<Analyze />'
AnalysisState_message = '<Prerequisite Key="Analyzing" Cookie="Prerequisite" Culture="en-US" />'
USS1 = '<ExecuteSequence Sequence="Unload Sample Step 1" />'
USS1 = '<ExecuteSequence Sequence="Unload Sample Step 2" />'

Reaming_message = '<ExecuteSequence Sequence="Ream Anode" Cookie="ExecuteSequence" Culture="en-US" />'
ReamState_message = '<Sequence Name="Ream Anode" Cookie="Sequence" Culture="en-US" />'

############### Define functions to handle PLC connection and Communication ###############
def handle_PLC_connection():
    global PLC_socket
    PLC_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        PLC_socket.connect((PLC_IP, PLC_PORT))
        PLC_socket.sendall("connect plc".encode(ENCODER))
        # Wait for a response to confirm connection
        response = PLC_socket.recv(BYTESIZE).decode(ENCODER)
        print(response)  # Should print "PLC Connection Established"
        print("PLC connection established")
        Wagon_Wheel_Initialization(data='default')
        return "PLC Connected"  # Return message indicating success
    except socket.error as e:
        print(f"Failed to connect to PLC: {e}")
        if PLC_socket:
            PLC_socket.close()
            PLC_socket = None

def close_PLC_connection():
    global PLC_socket
    if PLC_socket:
        print("Closing connection to PLC...")
        PLC_socket.close()
        PLC_socket = None
        print("Connection to PLC closed")

# NEED TO ADD FEW MORE THINGS ERIC
def send_receive_PLC(command): # function to send and receive commands to/from the PLC server
    """Send a command to the PLC and receive the response."""
    global PLC_socket
    if not PLC_socket:
        PLC_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PLC_socket.connect((PLC_IP, PLC_PORT))
    PLC_socket.sendall(command.encode(ENCODER))
    # Wait for a response to confirm the action
    response = PLC_socket.recv(BYTESIZE).decode(ENCODER)
    return response

############### Define functions to handle CORNERSTONE connection and communication ###############
def handle_CORNERSTONE_connection():
    global CORNERSTONE_socket
    try:
        if CORNERSTONE_socket is None:
            CORNERSTONE_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            CORNERSTONE_socket.connect((CORNERSTONE_SERVER_IP, CORNERSTONE_SERVER_PORT))
            print("Connected to CornerStone server.")
        return True
    except socket.error as e:
        print(f"Failed to connect to CornerStone: {e}")
        if CORNERSTONE_socket:
            CORNERSTONE_socket.close()
            CORNERSTONE_socket = None
        return False
    
#Check Error is not a query. It recieves the response when we send any message. It only tells us if the GDS
#recieved the message and if it is in the correct syntax
def checkError(error_response):
  root = ET.fromstring(error_response) #parse XML message
  error_message = root.attrib.get('ErrorMessage') #Isolate ErrorMessage
  #CHANGE MESSAGE SEEN
  if error_message == "Success":
      print("Logon Successful")
      return True
      #SIMPLY MOVE ON
  else:
      print("Logon failed: ", error_message)
      return False
      #Return Value that prompts error

#checkStringValue(SampleLoadState_reponse) takes the query message and returns a string with the Value attribute. 
#Basically it extracts the value that we are intrested in
def checkStringValue(SampleLoadState_reponse):
    root = ET.fromstring(SampleLoadState_reponse) # Parse the original XML message
    set_key = root.get('Value')# Extract the value of the 'Value' attribute
    print(set_key)
    return set_key

#checkReamStateValue(ReamState_response) takes a query message and returns 
#"True" or "False" Specifically for the ream step
#True - process is complete
#False - Process is still being executed
def checkReamStateValue(ReamState_response):
    root = ET.fromstring(ReamState_response) # Parse the XML message
    running_state = root.attrib.get('Running') # Get the 'Running' attribute
    print(ReamRunning_status)
    return ReamRunning_status

def checkAnalysisValue(SampleAnalysisState_response):
    root = ET.fromstring(SampleAnalysisState_response) # Parse the XML message
    running_state = root.attrib.get('Running') # Get the 'Running' attribute
    print(AnalysisRunning_state)
    return AnalysisRunning_state

def send_receive_CORNERSTONE(xml_command):
    """Send an XML command to the CornerStone server and receive the response."""
    global CORNERSTONE_socket
    if handle_CORNERSTONE_connection():  # Ensure connection is established
        # Prepare the XML command
        encoded_command = xml_command.encode(CORNERSTONE_ENCODER)
        # Send the length of the command followed by the command itself
        packed_length = struct.pack('<i', len(encoded_command))
        CORNERSTONE_socket.sendall(packed_length)
        CORNERSTONE_socket.sendall(encoded_command)
        
        # Receive the response length
        response_length_bytes = CORNERSTONE_socket.recv(4)
        if response_length_bytes:
            response_length = struct.unpack('<i', response_length_bytes)[0]
            # Receive the full response based on the length
            response = CORNERSTONE_socket.recv(response_length).decode(CORNERSTONE_ENCODER)
            print(f"Received from CornerStone: {response}")
            return response
    return None

def close_CORNERSTONE_connection():
    global CORNERSTONE_socket
    if CORNERSTONE_socket:
        print("Closing connection to CornerStone...")
        CORNERSTONE_socket.close()
        CORNERSTONE_socket = None
        print("Connection to CornerStone closed")

        

def Wagon_Wheel_Initialization(data):
    global wagon_wheel  # Declare the use of the global variable
    if data == '8-Spoke Wagon Wheel Selected':
        wagon_wheel = 8
        print("Sending 8-spoke selection to PLC...")
        send_receive_PLC("8-spoke")
    elif data == '16-Spoke Wagon Wheel Selected':
        wagon_wheel = 16
        print("Sending 16-spoke selection to PLC...")
        send_receive_PLC("16-spoke")
    else:
        # If no button is pressed, it defaults to 8 spokes
        print(f"No Wagon Wheel selection made yet, defaulting to {wagon_wheel}-spoke wheel.")
        send_receive_PLC("8-spoke")

################## Define State Classes ####################################################################

class State: # base parent state for all states
    def __init__(self, context, gui_client_socket, name):
        self.context = context
        self.gui_client_socket = gui_client_socket  # Store the gui_client_socket in each state
        self.name = name  # Add a name attribute to identify the state

    def handle(self, data):
        raise NotImplementedError("Each state must implement a handle method.")  #Forces every state class to implement its own version of the handle method

    def enter_state(self): # Every state class must have an enter state method
        # This method can be overridden by the same method within a subclass
        print(f"{type(self).__name__} Entered!!!")

########################################################################################################################
class IdleState(State):
    def __init__(self, context, gui_client_socket):
        super().__init__(context, gui_client_socket, name = "Idle State")  # Ensures State's initialization logic is executed

    def enter_state(self):
        super().enter_state() #executes enter_state() method in base state class
        # [INSERT] Code to execute every time the state is entered

    def handle(self, data): # Different commands that will execute when specific commands are sent to server instance while code in idle state
        #Handles commands specific to idle state
        print(f"Idle State: Received '{data}'")
        if data == "calibration on":
            self.context.change_state('calibration')
            send_receive_PLC(data)
        elif data == "Start Analysis Process": 
            self.context.change_state('analysis')
        elif data in ['8-Spoke Wagon Wheel Selected', '16-Spoke Wagon Wheel Selected']:
            Wagon_Wheel_Initialization(data)
        elif data == "connect plc request":
            # Simulate socket connection operation to PLC then sends confirmation upon connection to gui
            response = handle_PLC_connection()
            print(response)
            self.gui_client_socket.send(response.encode(ENCODER))
        elif data == "connect cornerstone request":
            # Simulate socket connection operation to Cornerstone then sends confirmation upon connection to gui
            CORNERSTONE_connection_status = handle_CORNERSTONE_connection()
            if CORNERSTONE_connection_status:
                print("Sending to GUI 'Cornerstone Connected'")
                gui_response = 'Cornerstone Connected'
                self.gui_client_socket.send(gui_response.encode(ENCODER))

########################################################################################################################
class CalibrationState(State):
    def __init__(self, context, gui_client_socket):
        super().__init__(context, gui_client_socket, name = "Calibration State")
        #self.initialized = False  # To track if the initial processes have been run

    def enter_state(self):
        super().enter_state()
        # Code to execute every time the state is entered
        self.start_calibration_process()

    def handle(self, data):
        if data == "calibration off":
            self.gui_client_socket.send("Calibration Mode: OFF".encode(ENCODER)) #send gui message that automatically turns buttons to off state
            send_receive_PLC(data) #send PLC calibration mode off
            self.context.change_state('idle')

    def start_calibration_process(self):
        print("Sending Calibration mode command to PLC...")
        self.gui_client_socket.send("Calibration Mode: ON".encode(ENCODER))
        PLC_response = send_receive_PLC("Enter Calibration Mode")
        if PLC_response:
            self.gui_client_socket.send("Calibration Mode: OFF".encode(ENCODER))
            self.context.change_state('idle')
        else:
            print("Calibration failed or not confirmed:", PLC_response)

########################################################################################################################
class AnalysisState(State):
    def __init__(self, context, gui_client_socket):
        super().__init__(context, gui_client_socket, name = "Analysis State")
        #     By passing self (the instance of AnalysisState) as the context to each sub-state, you effectively allow each sub-state
        # to have a direct link back to the parent state (AnalysisState). This setup lets them call change_sub_state and other 
        # functionalities provided by the parent state, enabling smooth transitions between sub-states.
        self.sub_states = { 
            'initializing': InitializingState(self, gui_client_socket, name = 'Analysis Sub-State: Initialization State'),
            'loading': LoadingState(self, gui_client_socket, name = 'Analysis Sub-State: Loading State'),
            'sample analyzing': SampleAnalysisState(self, gui_client_socket, name = 'Analysis Sub-State: Sample Analyze State'),
            'unloading': UnloadingState(self, gui_client_socket, name = 'Analysis Sub-State: Unloading State'),
            'reaming': ReamingState(self, gui_client_socket, name = 'Analysis Sub-State: Reaming State'),
            'moving': MovingState(self, gui_client_socket, name = 'Analysis Sub-State: Moving State')
        }
        self.current_sub_state = self.sub_states['initializing'] # can be thought of as context_sub_state
        self.is_active = False  # Initialize the is_active attribute to control process initiation

    def enter_state(self):
        super().enter_state()
        self.current_sub_state.enter_state()
        # Actions to execute when entering the analysis state
        #self.start_analysis_processes()
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
        elif data == "stop analysis":
            print("Stopping analysis processes...")
            self.context.change_state('idle')  # Optionally switch to idle state
            self.is_active = False
    
    def change_sub_state(self, sub_state_key):
        if sub_state_key in self.sub_states:
            self.current_sub_state = self.sub_states[sub_state_key]
            self.current_sub_state.enter_state()

########################################
class InitializingState(State):
    def enter_state(self):
        super().enter_state()
        self.send_logon()
        self.add_samples()

    def handle(self, data):
        print(f"Sent from main GUI: {data}")

    def add_samples(self):
        global wagon_wheel
        print(f"Adding {wagon_wheel} Samples...")
        if wagon_wheel == 16:
            addSample_response = send_receive_CORNERSTONE(AddSample16Spoke_XML)
            addSample_message_flag = checkError(addSample_response) # bool TRUE if success in message
            if addSample_message_flag:
                print("Commencing LRAS...")
                LRAS_response = send_receive_CORNERSTONE(LRAS_message)
                # Parse the original XML message
                root = ET.fromstring(LRAS_response)
                # Extract the value of the 'Key' attribute
                set_key = root.find('.//Set').get('Key')
                # New XML message
                ANTA_message = f'<AssignNextToAnalyze SetKey="{set_key}" ReplicateTag="0" />'
                ANTA_response = send_receive_CORNERSTONE(ANTA_message) 
                ANTA_message_flag = checkError(ANTA_response)
                if ANTA_message_flag:
                    print("Commencing disable auto-analyze")
                    DAA_response = send_receive_CORNERSTONE(DAA_message)
                    DAA_message_flag = checkError(DAA_response)
                    if DAA_message_flag:
                        #transition to loading state 
                        self.transition_sub_states()
                        #ADD A COMMAND HERE THAT TELLS THE PLC TO MOVE THE X-AXIS
            else:
                #ADD POSSIBLE ERROR STATE OR GO BACK TO IDLE STATE
                print("We screwed fs")
        else:
            addSample_response = send_receive_CORNERSTONE(AddSample8Spoke_XML)
        # Not sure but possibly need to add funcitonality to recieve messages

    def send_logon(self):
        print("sending logon information to Cornerstone...")
        login_response = send_receive_CORNERSTONE(Login_Password_XML)
        if 'Success' in login_response:
            print("Initialization State: Login successful.")
        else:
            print("Initialization State:Login failed.")
        # Possibly add command to send heartbeat to make sure connection has been established to cornerstone

    def transition_sub_states(self):
        # Assuming the next state after initialization is 'loading'
        print("Transitioning to Loading State...")
        time.sleep(2)
        self.context.change_sub_state('loading')
 
#########################################
class LoadingState(State):
    def enter_state(self):
        super().enter_state()
        self.execute_load_samples2()
        self.transition_sub_states()
        #Include the error stuff in this sub-class

    def handle(self, data):
        print(f"Sent from main GUI: {data}")
        if data == 'try again':
            #[INSERT FUNCTION FOR REDOING SAMPLE LOAD]
            self.handle_try_again()
            print("Retrying Sample Load")
        if data == 'skip spoke': 
            #[INSERT FUNCTION FOR MOVING ONTO NEXT SPOKE]
            self.handle_skip_spoke()
            print("Moving onto next spoke")
        if data == 'abort':
            #[INSERT FUNCTION FOR ABORTING ENTIRE ANALYSIS PROCESS]
            self.handle_abort()
            print("Aborting Process")


    def execute_load_samples1(self):
        print("Commencing sample step 1...")
        LSS1_response = send_receive_CORNERSTONE(LSS1)
        LSS1_message_flag = checkError(LSS1_response)
        if LSS1_message_flag:
            while True:
                SampleLoadState_response = send_receive_CORNERSTONE(SampleLoadState_message) #Sends query message to see if step is complete
                LSS1_SetKey = checkStringValue(SampleLoadState_response)
                time.sleep(1)
                if LSS1_SetKey == "Error: pressure evacuation timeout":
                    # POSSIBLY NEED TO PASS gui_client_socket
                    self.gui_client_socket.send("Vacuum Error".encode(ENCODER)) #tell gui.py to open vacuum error gui
                elif LSS1_SetKey == "Evacuated":
                    print("Commencing sample step 2...")
                    break
            self.execute_load_samples2()

    def execute_load_samples2(self):
        print("Commencing sample step 2...")
        LSS2_response = send_receive_CORNERSTONE(LSS2)
        LSS2_message_flag = checkError(LSS2_response)
        if LSS2_message_flag:
            while True:
                SampleLoadState_response = send_receive_CORNERSTONE(SampleLoadState_message) #Sends query message to see if step is complete
                LSS2_SetKey = checkStringValue(SampleLoadState_response)
                time.sleep(1)
                if LSS2_SetKey == "Error: depressurizing to 0.1 torr timeout":
                    # POSSIBLY NEED TO PASS gui_client_socket
                    self.gui_client_socket.send("Vacuum Error".encode(ENCODER)) #tell gui.py to open vacuum error gui
                elif LSS2_SetKey == "Clamped - Low Pressure":
                    print("Commencing sample step 3 (Reaming)...")
                    #WILL NEED TO SEND PLC A COMMAND TO UNDO THE X-AXIS
                    break
            self.execute_load_samples3()

    def execute_load_samples3(self): #Will not have an error, as it only reams
        print("Commencing sample step 3...")
        LSS3_response = send_receive_CORNERSTONE(LSS3)
        LSS3_message_flag = checkError(LSS3_response)
        if LSS3_message_flag:
            while True:
                SampleLoadState_response = send_receive_CORNERSTONE(SampleLoadState_message) #Sends query message to see if step is complete
                LSS3_SetKey = checkStringValue(SampleLoadState_response)
                time.sleep(1)
                if LSS3_SetKey == "Error: depressurizing to 0.1 torr timeout":
                    # POSSIBLY NEED TO PASS gui_client_socket
                    self.gui_client_socket.send("Vacuum Error".encode(ENCODER)) #tell gui.py to open vacuum error gui
                elif LSS2_SetKey == "Loaded":
                    print("Sample Loaded, Commencing Sample Analysis...")
                    #WILL NEED TO SEND PLC A COMMAND TO UNDO THE X-AXIS
                    break
            #LOADING STATE COMPLETE, EXECUTE ANALYSIS
            #transition to analysis state 
            self.transition_sub_states() #IS THIS THE CORRECT COMMAND?
            

    def transition_sub_states(self):
        print("Transitioning to Sample Analyze State...")
        time.sleep(2)
        self.context.change_sub_state('sample analyzing')
    
    def handle_try_again(self):
        print("Handling 'try again' command...")
        # Insert logic to retry the operation that failed
        # Try the same loading sample step again (whatever step is failed on)

    def handle_skip_spoke(self):
        print("Handling 'skip spoke' command...")
        # Insert logic to skip the current operation and move to the next

    def handle_abort(self):
        print("Handling 'abort' command...")
        # Insert logic to abort the operation and possibly reset or shutdown

##########################################
class SampleAnalysisState(State):
    def enter_state(self):
        super().enter_state()
        self.execute_sample_analysis()
        self.transition_sub_states()
        
    def handle(self, data):
        print(f"Sent from main GUI: {data}")

    def execute_sample_analysis(self):
        print("Conducting Sample Analysis...")
        SampleAnalysis_response = send_receive_CORNERSTONE(Analyze_Sample_message)
        SampleAnalysis_message_flag = checkError(SampleAnalysis_response)
        if SampleAnalysis_message_flag:
            while True:
                SampleAnalysisState_response = send_receive_CORNERSTONE(AnalysisState_message) 
                AnalysisRunning_state = checkAnalysisValue(SampleAnalysisState_response) 
                time.sleep(1)
                if AnalysisRunning_state == "true":  #Still running
                    continue #Break out of loop and send query again
                elif AnalysisRunning_state == "false": #Running complete
                    print('Analysis Complete, Commencing unloading ...')
                    break
            self.transition_sub_states()

    
    def transition_sub_states(self):
        print("Transitioning to Unloading State...")
        time.sleep(2)
        self.context.change_sub_state('unloading')

##########################################
class UnloadingState(State):
    def enter_state(self):
        super().enter_state()
        self.execute_unload_samples1()
        self.transition_sub_states()
        
    def handle(self, data):
        print(f"Sent from main GUI: {data}")

    def execute_unload_sample1(self):
        print("Commencing UNLOAD sample step 1...")
        ULSS1_response = send_receive_CORNERSTONE(USS1)
        USS1_message_flag = checkError(USS1_response)
        if USS1_message_flag:
            while True:
                SampleLoadState_response = send_receive_CORNERSTONE(SampleLoadState_message) #Sends query message to see if step is complete
                USS1_SetKey = checkStringValue(SampleLoadState_response)
                time.sleep(1)
                if USS1_SetKey == "Unclampled":
                    print("Commencing Unloade sample step 2...")
                    break
            self.execute_load_samples2()

    def execute_unload_sample2(self):
        print("Commencing UNLOAD sample step 2...")
        ULSS2_response = send_receive_CORNERSTONE(USS2)
        USS2_message_flag = checkError(USS2_response)
        if USS1_message_flag:
            while True:
                SampleLoadState_response = send_receive_CORNERSTONE(SampleLoadState_message) #Sends query message to see if step is complete
                USS2_SetKey = checkStringValue(SampleLoadState_response)
                time.sleep(1)
                if USS1_SetKey == "Released":
                    print("Moving Hardware out of the way")
                    #ADD SOMETHING HERE THAT COMMANDS THE PLC TO MOVE OUT THE WAY, A SIMPLE STRING
                    #WILL NEED TO ADD SOMETHING THAT WAITS FOR PLC TO SEND THAT THE MOTORS HAVE COMPETED THEIR MOVEMENT
                    break
                transition_sub_states()
    
    def transition_sub_states(self):
        print("Transitioning to Moving State...")
        time.sleep(2)
        self.context.change_sub_state('moving')

##########################################
class MovingState(State):
    def enter_state(self):
        super().enter_state()
        self.move_home()
        self.transition_sub_states()
        
    def handle(self, data):
        print(f"Sent from main GUI: {data}")

    def move_home(self):
        print("Moving sample to home position...")
    
    def transition_sub_states(self):
        print("Transitioning to Reaming State...")
        time.sleep(2)
        self.context.change_sub_state('reaming')

##########################################
class ReamingState(State):
    def enter_state(self):
        super().enter_state()
        self.ream_anode()
        self.transition_sub_states()
        
    def handle(self, data):
        print(f"Sent from main GUI: {data}")

    def ream_anode(self):
        print("Reaming GDS Anode...")
        Reaming_response = send_receive_CORNERSTONE(Reaming_message)
        SampleAnalysis_message_flag = checkError(Reaming_response)
        if SampleAnalysis_message_flag:
            while True:
                ReamState_response = send_receive_CORNERSTONE(ReamState_message) 
                Reaming_state = checkReamStateValue(ReamState_response) 
                time.sleep(1)
                if Reaming_state == "true":  #Still running
                    continue #Break out of loop and send query again
                elif Reaming_state == "false": #Running complete
                    print('Reaming Complete, Repeating Loading on new Spoke ...')
                    #SEND A MESSAGE TO PLC INDICATING IT TO MOVE TO THE NEXT SPOKE
                    #WE WILL WAIT UNTIL THE PLC RETURNS A MESSAGE SAYING THAT IT HAS COMPLTED MOVING
                    break
            self.transition_sub_states()

    
    def transition_sub_states(self):
        print("Transitioning back to Moving State...")
        time.sleep(2)
        self.context.change_sub_state('moving')

##########################################################################################################
# The Context class manages the high-level state transitions (like between IdleState, AnalysisState, and CalibrationState)
class Context:
    def __init__(self, gui_client_socket):
        self.gui_client_socket = gui_client_socket
        self.states = {  # each 'state' is like key that switches states based on it
            'idle': IdleState(self, gui_client_socket),
            'analysis': AnalysisState(self, gui_client_socket),
            'calibration': CalibrationState(self, gui_client_socket)
        }
        self.state = self.states['idle']
    
    def change_state(self, trans_state_name): # method that dictates transition between analysis, calibration, and idle states 
        # Conditions to allow state transition
        if self.state.name == "Idle State" and (trans_state_name == 'calibration' or trans_state_name == 'analysis'):
            print(f"Context: Transitioning from {self.state.name} to {trans_state_name} state.")
            self.state = self.states[trans_state_name]
            self.state.enter_state()
        elif (self.state.name == "Calibration State" or self.state.name == "Analysis State") and trans_state_name == 'idle':
            if self.state.name == "Analysis State" and trans_state_name == "analysis": #if press analysis button twice doesn't let you change states
                print("Already in Analysis State...")
            else:
                print(f"Context: Transitioning from {self.state.name} to {trans_state_name} state.")
                self.state = self.states[trans_state_name]
                self.state.enter_state()
        else:
            print("Transition not allowed: Must return to Idle state first or only transition to Idle from current state.")

    def handle(self, data):
        self.state.handle(data)

############################################################################################################
class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST_IP, HOST_PORT))
        self.server_socket.listen()

    def run(self):
        print("Server is running...")
        gui_client_socket, client_address = self.server_socket.accept()
        print(f"Connected to {client_address}")
        context = Context(gui_client_socket)  # Pass the client_socket to the context instance
        
        # try is the main code that is run and if anything goes wrong it moves to except block
        try:
            while True:
                data = gui_client_socket.recv(BYTESIZE).decode(ENCODER)
                if data == 'quit':
                    print("Server stopping...")
                    break
                else:
                    context.handle(data)  # Use the local 'context' object to handle data
        except Exception as e:  # error handling block
            print(f"An error occurred: {e}")
        # The finally block will execute no matter if the try block raises an error or not. ensures that the gui_client_socket and 
        #  self.server_socket are closed.
        finally: 
            gui_client_socket.close()
            self.server_socket.close()
            close_PLC_connection()  # Ensure PLC connection is closed on server shutdown
            close_CORNERSTONE_connection()  # Ensure CORNERSTONE connection is closed on server shutdown

################################################
# Creating server instance 
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

