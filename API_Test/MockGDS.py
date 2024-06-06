#
import socket
import struct
import xml.etree.ElementTree as ET
import time

# Define server constants
SERVER_IP = 'localhost'
SERVER_PORT = 12345
ENCODER = 'utf-16le'
BYTESIZE = 1024

# Define initial state
current_state = None
analyze_in_progress = False
ream_anode_state = 0  # New state variable for the Ream Anode sequence
logged_in = False  # Track if the client is logged in

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

# Define state-based response mapping NO VACUUM ERROR
state_response_map = {
    'Load Sample Step 1': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Evacuated" Cookie="StringValue" />',
    'Load Sample Step 2': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Clamped - Low Pressure" Cookie="StringValue" />',
    'Load Sample Step 3': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Loaded" Cookie="StringValue" />',
    'Unload Sample Step 1': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Unclamped" Cookie="StringValue" />',
    'Unload Sample Step 2': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Released" Cookie="StringValue" />'
}


# # Define state-based response mapping WITH VACUUM ERROR
# state_response_map = {
#     'Load Sample Step 1': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Error: pressure evacuation timeout" Cookie="StringValue" />',
#     'Load Sample Step 2': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Clamped - Low Pressure" Cookie="StringValue" />',
#     'Load Sample Step 3': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Loaded" Cookie="StringValue" />',
#     'Unload Sample Step 1': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Unclamped" Cookie="StringValue" />',
#     'Unload Sample Step 2': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Released" Cookie="StringValue" />'
# }


# Define message-response mapping
message_response_map = { 
    '<Logon User="156a" Password="156a156a"/>': '<Logon ErrorCode="0" ErrorMessage="Success" Cookie="Logon" />',
    AddSample8Spoke_XML : '<AddSamples ErrorCode="0" ErrorMessage="Success" Cookie="AddSamples" />',
    AddSample8Spoke_XML : '<AddSamples ErrorCode="0" ErrorMessage="Success" Cookie="AddSamples" />',
    '<LastRemoteAddedSets Cookie="LastRemoteAddedSets" Culture="en-US" />': '<LastRemoteAddedSets ErrorCode="0" ErrorMessage="Success" Cookie="LastRemoteAddedSets"><Set Key="0000000000007987" /></LastRemoteAddedSets>',
    '<AssignNextToAnalyze SetKey="0000000000007987" ReplicateTag="0" />': '<AssignNextToAnalyze ErrorCode="0" ErrorMessage="Success" Cookie="AssignNextToAnalyze" />',
    '<AutoAnalyze State="DISABLED" />': '<AutoAnalyze ErrorCode="0" ErrorMessage="Success"/>',
    '<ExecuteSequence Sequence="Load Sample Step 1" />': '<ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />',
    '<ExecuteSequence Sequence="Load Sample Step 2" />': '<ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />',
    '<ExecuteSequence Sequence="Load Sample Step 3" />': '<ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />',
    '<Analyze />': '<Analyze ErrorCode="0" ErrorMessage="Success" Cookie="3c1e171c-25d0-41e6-a67a-ee2a941c4cea" />',
    '<ExecuteSequence Sequence="Unload Sample Step 1" />': '<ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />',
    '<ExecuteSequence Sequence="Unload Sample Step 2" />': '<ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />'
}

# Function to handle client connection
def handle_client_connection(client_socket):
    global current_state, analyze_in_progress, ream_anode_state, logged_in
    try:
        while True:
            # Read the length of the incoming message (4 bytes)
            response_length_bytes = client_socket.recv(4)
            if not response_length_bytes:
                break  # Connection closed

            # Unpack the message length
            response_length = struct.unpack('<i', response_length_bytes)[0]

            # Read the incoming message based on the length
            incoming_message = client_socket.recv(response_length).decode(ENCODER)
            print(f"Received: {incoming_message}")

            # Determine the response based on the incoming message
            response_message = None

            if incoming_message == '<Logon User="156a" Password="156a156a"/>':
                response_message = message_response_map[incoming_message]
                logged_in = True
                print("Client logged in successfully.")
            elif logged_in:
                if incoming_message in message_response_map:
                    response_message = message_response_map[incoming_message]
                    if '<ExecuteSequence' in incoming_message:
                        root = ET.fromstring(incoming_message)
                        current_state = root.attrib.get('Sequence')
                        print(f"Current state updated to: {current_state}")
                elif incoming_message.startswith('<ExecuteSequence') and 'Sequence="Ream Anode"' in incoming_message:
                    print(f"Handling Ream Anode sequence, current ream_anode_state: {ream_anode_state}")
                    if ream_anode_state == 0:
                        # First part of the Ream Anode sequence
                        response_message = '<ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />'
                        ream_anode_state = 1
                    elif ream_anode_state == 1:
                        # Second part of the Ream Anode sequence
                        time.sleep(1)
                        response_message = '<Sequence ErrorCode="0" ErrorMessage="Success" Name="Ream Anode" Running="false" LastReturnResult="" Cookie="Sequence" />'
                        ream_anode_state = 0
                elif incoming_message.startswith('<Sequence') and 'Name="Ream Anode"' in incoming_message:
                    if ream_anode_state == 1:
                        time.sleep(1)
                        response_message = '<Sequence ErrorCode="0" ErrorMessage="Success" Name="Ream Anode" Running="false" LastReturnResult="" Cookie="Sequence" />'
                        ream_anode_state = 0
                    else:
                        response_message = '<Error>Invalid Ream Anode state</Error>'
                elif incoming_message == '<StringValue Key="Sample Load State" Cookie="StringValue" Culture="en-US" />':
                    if current_state in state_response_map:
                        response_message = state_response_map[current_state]
                    else:
                        response_message = '<Error>State not recognized</Error>'
                elif incoming_message == '<Prerequisite Key="Analyzing" Cookie="Prerequisite" Culture="en-US" />':
                    if analyze_in_progress:
                        time.sleep(2)  # Simulate analysis time
                        analyze_in_progress = False
                        response_message = '<Prerequisite ErrorCode="0" ErrorMessage="Success" Name="Analyzing" Value="false" Cookie="Prerequisite" />'
                    else:
                        response_message = '<Prerequisite ErrorCode="0" ErrorMessage="Success" Name="Analyzing" Value="false" Cookie="Prerequisite" />'
                else:
                    response_message = '<Error>Unknown message</Error>'
                    print(f"Unknown message received: {incoming_message}")
            else:
                response_message = '<Error>ErrorMessage="Not logged in" />'
                print("Client not logged in.")

            if incoming_message == '<Analyze />':
                analyze_in_progress = True

            # Send the response message
            if response_message is not None:
                if not (incoming_message == '<Prerequisite Key="Analyzing" Cookie="Prerequisite" Culture="en-US" />' and analyze_in_progress):
                    time.sleep(1)  # Introduce a 2-second delay for most messages
                encoded_response = response_message.encode(ENCODER)
                response_length = len(encoded_response)
                packed_length = struct.pack('<i', response_length)

                client_socket.send(packed_length)
                client_socket.send(encoded_response)
                print(f"Sent: {response_message}")
            else:
                print("No response message generated")
    finally:
        client_socket.close()

# Function to start the server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen()
        print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            handle_client_connection(client_socket)

# Start the server
if __name__ == "__main__":
    start_server()
