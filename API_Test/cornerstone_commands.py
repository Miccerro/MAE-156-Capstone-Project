import socket
import time
import xml.etree.ElementTree as ET
import select
import struct

# Define constants
#DESTINATION_IP = '10.10.10.2'  # IP address of PC
DESTINATION_IP = "127.0.0.1"
DESTINATION_PORT = 12345
ENCODER = "utf-16le"  # Character encoding scheme
BYTESIZE = 1024

def GDS_Connect():
    """
    Establishes a connection to the GDS and returns the socket.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((socket.gethostbyname(DESTINATION_IP), DESTINATION_PORT))

    print("Client_Socket in GDS_COnnect:", client_socket)
    return client_socket


def sendMessage(message, client_socket):
    print("Send Message:", message) #Simply prints the message to be sent
    encoded = message.encode(ENCODER) #encodes message
    length = len(encoded)
    packed = struct.pack('<i', length) #packs the length of the encoded message into binary format

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

def checkError(error_response):
    root = ET.fromstring(error_response) #parse XML message
    error_message = root.attrib.get('ErrorMessage') #Isolate ErrorMessage

    #CHANGE MESSAGE SEEN
    if error_message == "Success":
        print("Logon Successful")
        #SIMPLY MOVE ON
    else:
        print("Logon failed: ", error_message)
        #Return Value that prompts error 

def heartbeat(client_socket):
    heartbeat_message = '<Heartbeat />'
    sendMessage(heartbeat_message, client_socket)

def logon(client_socket):
    logon_message = '<Logon User="156a" Password="156a156a"/>' 
    logon_response = sendMessage(logon_message, client_socket)
    #Expected Reply: <Logon ErrorCode="0" ErrorMessage="Success" Cookie="Logon" />
    checkError(logon_response)

def addsamples(client_socket):
    ##WILL HAVE TO CHANGE BASED UPON IF WE WANT 8 or 16 SPOKES
    addsample8Spoke_message = '''
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
    addsample_reponse = sendMessage(addsample8Spoke_message,client_socket)

    checkError(addsample_reponse) #checks response

def LastRemoteAddedSets(client_socket):
  LRAS_message = '<LastRemoteAddedSets Cookie="LastRemoteAddedSets" Culture="en-US" />'
  #LRAS_message = '<LastRemoteAddedSets />'

  LRAS_Response = sendMessage(LRAS_message,client_socket)

  checkError(LRAS_Response)

  #print(LRAS_Response)
  return LRAS_Response



  #Expected Reply:
  # <LastRemoteAddedSets ErrorCode="0" ErrorMessage="Success" Cookie="LastRemoteAddedSets">
  # <Set Key="00000000000079F4" />
  # <Set Key="00000000000079F5" />
  # <Set Key="00000000000079F6" />
  # <Set Key="00000000000079F7" />
  # <Set Key="00000000000079F8" />
  # </LastRemoteAddedSets>


    

def AssignNextToAnalyze(LRAS_response,client_socket):
    #print(LRAS_response)
    # Parse the original XML message
    root = ET.fromstring(LRAS_response)
    # Extract the value of the 'Key' attribute
    set_key = root.find('.//Set').get('Key')
    # New XML message
    #ANTA_message = f'<AssignNextToAnalyze SetKey="{set_key}" ReplicateTag="0" />'
    ANTA_message = f'<AssignNextToAnalyze SetKey="{set_key}" ReplicateTag="0" />'
    ANTA_response = sendMessage(ANTA_message,client_socket)

    #Expected Reply: <AssignNextToAnalyze ErrorCode="0" ErrorMessage="Success" Cookie="AssignNextToAnalyze" />
    checkError(ANTA_response)

    

def DisableAutoAnalyze(client_socket):
    DAA = '<AutoAnalyze State="DISABLED" />'
    DAA_response = sendMessage(DAA,client_socket)

    #Expected reply: <AutoAnalyze ErrorCode=”0” ErrorMessage=”Success”/>
    checkError(ANTA_response)

def LoadSampleStep1(client_socket):
    LSS1 = '<ExecuteSequence Sequence="Load Sample Step 1" />'
    LSS1_response = sendMessage(LSS1,client_socket)
    
    #Expected Replies: <ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />
    checkError(LSS1_response)


def LoadSampleStep2(client_socket):
    LSS2 = '<ExecuteSequence Sequence="Load Sample Step 2" />'
    LSS2_response = sendMessage(LSS2,client_socket)

    #Expected Reply: <ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />
    checkError(LSS2_response)

def LoadSampleStep3(client_socket):
    LSS3 = '<ExecuteSequence Sequence="Load Sample Step 3" />'
    LSS3_response = sendMessage(LSS3,client_socket)

    #Expected Reply: <ExecuteSequence ErrorCode="0" ErrorMessage="Success" Cookie="ExecuteSequence" />
    checkError(LSS3_response)




def Analyze(client_socket):
    Analyze_message = '<Analyze />'
    Analyze_response = sendMessage(Analyze_message,client_socket)

    checkError(Analyze_response)


def UnloadSampleStep1(client_socket): 
    USS1 = '<ExecuteSequence Sequence="Unload Sample Step 1" />'
    USS1_response = sendMessage(USS1,client_socket)

    
    checkError(USS1_response)

def UnloadSampleStep2(client_socket):
  USS2 = '<ExecuteSequence Sequence="Unload Sample Step 2" />'
  USS2_response = sendMessage(USS2,client_socket)


  checkError(USS2_response)

def UnloadSampleStep3(client_socket):
  USS3 = '<ExecuteSequence Sequence="Unload Sample Step 3" />'
  USS3_response = sendMessage(USS3,client_socket)

  
  checkError(USS3_response)



def checkStringValue(SampleLoadState_reponse):
    root = ET.fromstring(SampleLoadState_reponse) # Parse the original XML message
    set_key = root.get('Value')# Extract the value of the 'Value' attribute

    print(set_key)
    return set_key

  
def LoadStateString(client_socket): #The State for all states are unique, we can reuse the same logic or can incorporate them into each function
  while True:
    time.sleep(1)
    SampleLoadState_message = '<StringValue Key="Sample Load State" Cookie="StringValue" Culture="en-US" />'
    SampleLoadState_reponse = sendMessage(SampleLoadState_message,client_socket)

    set_key = checkStringValue(SampleLoadState_reponse)


    
    ############# CHECK FOR STEP 1 ############# Creates Vacuum
    #Other messages: 
    #"Evacuating" (Start of load step 1)
    #"Evacuated" (Load step 1 complete)
    #Error: pressure evacuation timeout (Load Step 1 error)
    if set_key == "Error: pressure evacuation timeout":
      print("STEP 1 FAILED")
      #PLACE WHATEVER CODE WE WANT TO EXECUTE HERE, MAYBE OPEN GUI OR RETURN VALUE TO MAIN WHERE THEN THE ERROR GUI IS OPENED
    elif set_key == "Evacuated":
      print("STEP 1 COMPLETE READY TO MOVE ON TO NEXT STEP") 
      #PLACE WHATEVER CODE WE WANT TO EXECUTE HERE, MOVE ON TO NEXT STEP OR RETURN VALUE BACK TO MAIN TO THEN USE TO MOVE ONTO NEXT STATE
  
  
    ############# CHECK FOR STEP 2 ############# Pushes Puck on Sample
    #Other messages:
    elif set_key == "Error: depressurizing to 0.1 torr timeout": #Step 2 error
      print("STEP 2 FAILED")
      #PLACE CODE TO BE EXECUTED HERE
    elif set_key == "Clamped - Low Pressure": #Step 2 Competed
      print("STEP 2 COMPLETE READY TO MOVE ON TO NEXT STEP")

    ############# CHECK FOR STEP 3 #############
    #"Depressurizing to 0.1 torr" (In the process)
    #"Preparing" (Pressurizing lamp)
    #Loaded (Complete entire process)
    elif set_key == "Error: depressurizing to 0.1 torr timeout": #Step 3 error
      print("STEP 3 FAILED")
      #PLACE CODE TO BE EXECUTED HERE
    elif set_key == "Loaded": #Step 3 Competed
      print("STEP 3 COMPLETE READY TO MOVE ON TO NEXT STEP")

    ############# CHECK FOR UNLOAD STEP 1 #############
    #"Unclamping" (Start of Unload Step 1)
    #"Preparing" (Pressurizing lamp)
    #Loaded (Complete entire process)
    elif set_key == "Unclamped": #Step 1 Complete
      print("UNLOAD STEP 2 COMPLETE")
      #PLACE CODE TO BE EXECUTED HERE

    ############# CHECK FOR UNLOAD STEP 2 #############
    elif set_key == "Released": #Step 2 Complete
      print("UNLOAD STEP 2 COMPLETE")
      #PLACE CODE TO BE EXECUTED HERE

    ############# CHECK FOR UNLOAD STEP 3 #############
    elif set_key == "No Sample": #Step 3 Complete
      print("UNLOAD STEP 3 COMPLETE")
      #PLACE CODE TO BE EXECUTED HERE

    #Unload step 3 complete. Anode cleaning complete, no sample on lamp, door unlocked.
    #Do I need to do 3 to get another reading?

    else:
      print(f"Received unexpected value: {set_key}")
      continue  # Keep looping and querying for the desired state

    break  # Exit the loop if we handled a known state


####### Beggining of process ######

client_socket = GDS_Connect() #Connect to CornerStone
input("Press Enter to continue. Connect Complete, logon is next")
logon(client_socket) #logon to acess commands
input("Press Enter to continue. Add Samples is next")
addsamples(client_socket) #Add sample (For 8 spoke wagon wheel)
input("Press Enter to continue. Obtain SetKey")
LRAS_response = LastRemoteAddedSets(client_socket) #Obtain set key
input("Press Enter to continue. AssignNextToAnalyze")
AssignNextToAnalyze(LRAS_response,client_socket) #Specify what set key to analyze next 



#for troubleshooting purposes leave AutoAnlyze off
# input("Press Enter to continue. Disable Auto Analyze is next")
# DisableAutoAnalyze(client_socket)
input("Press Enter to continue. Load Sample Step 1 is next")
LoadSampleStep1(client_socket)
input("Press Enter to continue. Query LSS1")
LoadStateString(client_socket)
input("Press Enter to continue. Load Sample Step 2 is next")
LoadSampleStep2(client_socket)
input("Press Enter to continue. Query LSS2")
LoadStateString(client_socket)
input("Press Enter to continue. Load Sample Step 3 is next close door before hitting enter")
LoadSampleStep3(client_socket)
input("Press Enter to continue. Query LSS3")
LoadStateString(client_socket)
input("Press Enter to continue. Analyze is next")
Analyze(client_socket)
input("Press Enter to continue. Unload Sample Step 1 is next")
UnloadSampleStep1(client_socket)
input("Press Enter to continue. Query USS1")
LoadStateString(client_socket)
input("Press Enter to continue. Unload Sample Step 2 is next")
UnloadSampleStep2(client_socket)
input("Press Enter to continue. Query USS2")
LoadStateString(client_socket)
input("Press Enter to continue. Unload Sample Step 3 is next")
UnloadSampleStep2(client_socket)
input("Press Enter to continue. Query USS3")
LoadStateString(client_socket)



# #Get ready for next analysis (NUMBER 2)
# input("Press Enter to continue. AssignNextToAnalyze")
# AssignNextToAnalyze(LRAS_response,client_socket) #Specify what set key to analyze next (WILL AUTO PICK NEXT REPLICATE)
# input("Press Enter to continue. Load Sample Step 1 is next")
# LoadSampleStep1(client_socket)
# input("Press Enter to continue. Load Sample Step 2 is next")
# LoadSampleStep2(client_socket)
# input("Press Enter to continue. Load Sample Step 3 is next close door before hitting enter")
# LoadSampleStep3(client_socket)
# input("Press Enter to continue. Analyze is next")
# Analyze(client_socket)

# #Get ready for next analysis (NUMBER 3)
# input("Press Enter to continue. AssignNextToAnalyze")
# AssignNextToAnalyze(LRAS_response,client_socket) #Specify what set key to analyze next (WILL AUTO PICK NEXT REPLICATE)
# input("Press Enter to continue. Load Sample Step 1 is next")
# LoadSampleStep1(client_socket)
# input("Press Enter to continue. Load Sample Step 2 is next")
# LoadSampleStep2(client_socket)
# input("Press Enter to continue. Load Sample Step 3 is next close door before hitting enter")
# LoadSampleStep3(client_socket)
# input("Press Enter to continue. Analyze is next")
# Analyze(client_socket)






