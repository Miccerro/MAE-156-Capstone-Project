import xml.etree.ElementTree as ET


SampleLoadState_reponse = '<StringValue ErrorCode="0" ErrorMessage="Success" Name="Sample Load State" Value="Clamped - Low Pressure" Cookie="StringValue" />'

# Parse the original XML message
root = ET.fromstring(SampleLoadState_reponse)
print(root)
# Extract the value of the 'Key' attribute
set_key = root.get('Value')
print(set_key)

import xml.etree.ElementTree as ET

logon_response = '''<LastRemoteAddedSets ErrorCode="0" ErrorMessage="Success" Cookie="LastRemoteAddedSets">
  # <Set Key="00000000000079F4" />
  # <Set Key="00000000000079F5" />
  # <Set Key="00000000000079F6" />
  # <Set Key="00000000000079F7" />
  # <Set Key="00000000000079F8" />
  # </LastRemoteAddedSets>'''

def checkError(error_response):
    root = ET.fromstring(error_response) #parse XML message
    error_message = root.attrib.get('ErrorMessage') #Isolate ErrorMessage

    if error_message == "Success":
        print("Logon Successful")
        #SIMPLY MOVE ON
    else:
        print("Logon failed: ", error_message)
        #Return Value that prompts error 

checkError(logon_response)














# # Original XML message
# LRAS_response = '''
# <LastRemoteAddedSets ErrorCode="0" ErrorMessage="Success" Cookie="LastRemoteAddedSets">
#   <Set Key="0000000000007987" />
# </LastRemoteAddedSets>
# '''

# # Parse the original XML message
# root = ET.fromstring(LRAS_response)

# # Extract the value of the 'Key' attribute
# set_key = root.find('.//Set').get('Key')

# # New XML message
# ANTA_message = f'<AssignNextToAnalyze SetKey="{set_key}" ReplicateTag="" />'

# print(ANTA_message)

#############

def sendMessage(message):
    print("Send Message:", message) #Simply prints the message to be sent
    encoded = message.encode(ENCODER) #encodes message
    length = len(encoded)
    packed = struct.pack('<i', length) #packs the length of the encoded messafe into binary format

    # send data length
    client_socket.send(packed)
    # send encoded data
    client_socket.send(encoded)

    # read response length
    responseLengthBytes = client_socket.recv(4) #Recieves response length in bytes
    responseLength = struct.unpack('<i', responseLengthBytes)[0] #unpacks recieved bytes back into integer
    print("Message Response Length:", responseLength)
    # read response data
    response = client_socket.recv(responseLength).decode(ENCODER)
    print("Message Response:", response)
    return response

def heartbeat():
    heartbeat_message = '<Heartbeat />'
    HB_response = sendMessage(heartbeat_message)

    return HB_response

def version():
    sendMessage('<Version/>')

# GDS_Connect()
# input("Press Enter to continue. Connect Complete, Heartbeat next")
# heartbeat()
# input("Press Enter to continue. Version next")
# version()
