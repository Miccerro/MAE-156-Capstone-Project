import socket
import struct
import xml.etree.ElementTree as ET

# Define server constants
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
ENCODER = 'utf-16le'
BYTESIZE = 1024

# Define initial state
current_state = None

# Define state-based response mapping
state_response_map = {
    'Load Sample Step 1': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Evacuated" Cookie="StringValue" />',
    'Load Sample Step 2': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Clamped - Low Pressure" Cookie="StringValue" />',
    'Load Sample Step 3': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Loaded" Cookie="StringValue" />',
    '<Analyze />': '...',
    'Unload Sample Step 1': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Unclamped" Cookie="StringValue" />',
    'Unload Sample Step 2': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Released" Cookie="StringValue" />',
    'Unload Sample Step 3': '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="No Sample" Cookie="StringValue" />'
} #WILL HAVE TO CHANGE VALUE BY HAND

# Define message-response mapping
message_response_map = {
    '<Logon User="156a" Password="156a156a"/>': '<Logon ErrorCode="0" ErrorMessage="Success" Cookie="Logon" />',
    '''
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
''': '<AddSamples ErrorCode="0" ErrorMessage="Success" Cookie="AddSamples" />',
    '<LastRemoteAddedSets Cookie="LastRemoteAddedSets" Culture="en-US" />': '''<LastRemoteAddedSets ErrorCode="0" ErrorMessage="Success" Cookie="LastRemoteAddedSets">
  <Set Key="0000000000007987" />
</LastRemoteAddedSets>''',
    '<AssignNextToAnalyze SetKey="0000000000007987" ReplicateTag="0" />': '<AssignNextToAnalyze ErrorCode="0" ErrorMessage="Success" Cookie="AssignNextToAnalyze" />',
    '<AutoAnalyze State="DISABLED" />': '<AutoAnalyze ErrorCode="0" ErrorMessage="Success"/>',
    '<ExecuteSequence Sequence="Load Sample Step 1" />': '<ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />',
    '<ExecuteSequence Sequence="Load Sample Step 2" />': '<ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />',
    '<ExecuteSequence Sequence="Load Sample Step 3" />': '<ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />',
    '<Analyze />': '<Analyze ErrorCode="0" ErrorMessage="Success" Cookie="3c1e171c-25d0-41e6-a67a-ee2a941c4cea" />',
    '<ExecuteSequence Sequence="Unload Sample Step 1" />': '<ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />',
    '<ExecuteSequence Sequence="Unload Sample Step 2" />':'<ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />',
    '<ExecuteSequence Sequence="Unload Sample Step 3" />':'<ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />',
    #'<StringValue Key="Sample Load State" Cookie="StringValue" Culture="en-US" />':
    # Add more message-response pairs as needed
}

def handle_client_connection(client_socket):
    global current_state
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
            if incoming_message in message_response_map:
                response_message = message_response_map[incoming_message]
                if '<ExecuteSequence' in incoming_message:
                    root = ET.fromstring(incoming_message)
                    current_state = root.attrib.get('Sequence')
            elif incoming_message == '<StringValue Key="Sample Load State" Cookie="StringValue" Culture="en-US" />':
                if current_state in state_response_map:
                    response_message = state_response_map[current_state]
                else:
                    response_message = '<Error>State not recognized</Error>'
            else:
                response_message = '<Error>Unknown message</Error>'

            # Send the response message
            encoded_response = response_message.encode(ENCODER)
            response_length = len(encoded_response)
            packed_length = struct.pack('<i', response_length)

            client_socket.send(packed_length)
            client_socket.send(encoded_response)
            print(f"Sent: {response_message}")
    finally:
        client_socket.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen()
        print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            #print(f"Connection from {client_address}")
            handle_client_connection(client_socket)

# Start the server
if __name__ == "__main__":
    start_server()

