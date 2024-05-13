#networking to the GDS:
#Assume that the PC (where this code will be executed) is our Client
import socket
import xml.etree.ElementTree as ET
import time
import select

#Define constants
DESTINATION_IP = '10.10.10.2' #IP address of PLC
DESTINATION_PORT = 12345
ENCODER = "utf-16" #NOTE: Normally this is utf-8, they are different character encoding schemes (just keep consistant)
BYTESIZE = 1024

def GDS_Connect():
    #Cretea a clientside IPv4 socekt (AF_INET) and TCP (SOCK_STREAM) //Just specifies what to use
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect( (socket.gethostbyname(DESTINATION_IP), DESTINATION_PORT) ) #sent socket to specific location
    #client will wait and listine here //NOTE: IP address will have to be changed to connect to GDS900 (if not already)
    #print("Executed Connection Code")

    #Will have to determine when to close the socket some other time, likely when the analysis is all complete.

    return client_socket


client_socket = GDS_Connect()

def GDS_Disconnect():
    disconnect_message = '<Disconnect/>'
    client_socket.send(disconnect_message.encode(ENCODER))

def heartbeat(client_socket):
    #client_socket = GDS_Connect()
    #Define XML messages to be sent over:
    heartbeat_message = '<Heartbeat/>'
    client_socket.send(heartbeat_message.encode(ENCODER))

    #We will receive something like: <Heartbeat ErrorCode=”0” ErrorMessage=”Success”/>
    #Is the message immediate? If not how can i delay the decoding of the message? Do i have to ask state via Query, or can is the reply enough? Do i need a delay?
    #Something with the cookies attribute?

    HB_response = client_socket.recv(BYTESIZE).decode(ENCODER) #NOTE: it isnt highlighted, so fine? "client_socket"
    print("Heartbeat Resposne:", HB_response)

    return HB_response

#In our test we were able to connect and subsequently disconnect. However, when running heartbeat, we are unable to recieve the reply.
    



def GDS_Logon(client_socket):
    logon_message = '<Logon User="156a" Password="156a156a"/>' #Again, "" is of concern
    client_socket.send(logon_message.encode(ENCODER))

    #We will receive something like: <Logon ErrorCode=”0” ErrorMessage=”Success”/>
    #Is the message immediate? If not how can i delay the decoding of the message? Do i have to ask state via Query, or can is the reply enough?

    logon_response = client_socket.recv(BYTESIZE).decode(ENCODER) #NOTE: it isnt highlighted, so fine? "client_socket"
    print("Logon Response:", logon_response)

    logon_root = ET.fromstring(logon_response) #Obtains root from xml message
    # Read the value of the 'ErrorMessage' attribute
    Logon_State = logon_root.get('ErrorMessage')
    print(Logon_State)

    if Logon_State == "Success":
        print("Login is a success.") #Will replace this with some function to next be exectued, or some tag saying to move onto the next step. Still gotta wrtite this out
    else:
        print(Logon_State) #Will print error

def AddSamples(client_socket):
    AddSample_message = '''
    <AddSamples>
  <PromptOperatorForEntry>True</PromptOperatorForEntry>
  <Set>
    <Field Id=”SampleTypehere”></Field>
    <Field Id=”SampleNameHere”></Field>
    <Field Id=”Description”></Field>
    <Field Id=”CdpMethodKey”>0</Field>
    <Field Id=”StandardKey”>0</Field>
    <Field Id=”UDF: 1111”>User defined field value here</Field>
    <Field Id=”SetId”>Set 1</Field>
  </Set>
  <Replicates>
    <Replicate>
      <Field Id=”Comments”></Field>
      <Field Id=”UDF: 1234”>User defined field value here</Field>
      <Field Id=”RepId”>Rep 1</Field>
    </Replicate>
    <Replicate>
      <Field Id=”Comments”></Field>
      <Field Id=”UDF: 1234”>User defined field value here</Field>
      <Field Id=”RepId”>Rep 2</Field>
    </Replicate>  
   </Replicates>
    </AddSamples>
'''
    client_socket.send(AddSample_message.encode(ENCODER))

    AddSample_response = client_socket.recv(BYTESIZE).decode(ENCODER) 
    print("AddSample Response:", AddSample_response)

def LastRemoteAddedSets():
    #Send XML Message
    LRAS_message = '<LastRemoteAddedSets/>' #Again, "" is of concern
    client_socket.send(LRAS_message.encode(ENCODER))

    #Recieve XML Message
    LRAS_response = client_socket.recv(BYTESIZE).decode(ENCODER) #NOTE: it isnt highlighted, so fine? "client_socket"
    print("LastRemoteAddedSets Response:", LRAS_response)

    #Parse 
    LRAS_root = ET.fromstring(LRAS_response)
    #Get the value of the Error Message Attribute:
    LRAS_error_message = LRAS_root.get('ErrorMessage')
    print("LRAS Error Message:", LRAS_error_message)
    #Gets the ("Set") Element and attribute 
    set_element = LRAS_root.find('.//Set') #.// syntax is on lib website
    key_value = set_element.get('Key')
    print("Key Attribute Value within Set:",key_value)

    #return key_value


def AssignNextToAnalyze(client_socket):
    ANTA_message = '<AssignNextToAnalyze SetKey="1234" ReplicateTag="1" />' #Alternatively <AssignNextToAnalyze SetKey="1234"/>
    client_socket.send(ANTA_message.encode(ENCODER))

    #Expected Reply: <AssignNextToAnalyze ErrorCode=”0” ErrorMessage=”Success”/>
    ANTA_response = client_socket.recv(BYTESIZE).decode(ENCODER) #NOTE: it isnt highlighted, so fine? "client_socket"
    print("AssignNextToAnalyze Response:", ANTA_response)

    #Parse 
    ANTA_root = ET.fromstring(ANTA_response)
    #Get the value of the Error Message Attribute:
    ANTA_error_message = ANTA_root.get('ErrorMessage')
    print("ANTA Error Message:", ANTA_error_message)
    #Gets the ("Set") Element and attribute 
    if ANTA_error_message == "Success":
        print("ANTA Ran Successfully")
        #Can place next method here to keep running
    else:
        print("ANTA Failed:", ANTA_error_message)



#Because load sample does not have a response, then we will have to go through a loop:

def LoadSample(client_socket):
    #Clamps Sample
    Load_S2 = '<ExecuteSequence Sequence="Load Sample Step 2"/>'
    client_socket.send(Load_S2.encode(ENCODER))
    time.sleep(10) #A delay for now, we can add a query that will loop through and move on to the next step only when finished
    
    #Unknown, but vital step
    Load_S1 = '<ExecuteSequence Sequence="Load Sample Step 1"/>'
    client_socket.send(Load_S1.encode(ENCODER))
    time.sleep(10) #Again, Query here instead. Delay for 10s

    #Sets Vaccum
    Load_S3 = '<ExecuteSequence Sequence="Load Sample Step 3"/>'
    client_socket.send(Load_S3.encode(ENCODER))
    time.sleep(10)

def Analyze():
    Analyze = '<ExecuteSequence Sequence="Analyze"/>'
    client_socket.send(Analyze.encode(ENCODER))




# # Main function 
# def main():
#     #GDS_Connect()
#     input("Press Enter to continue...")
#     GDS_Logon()

# if __name__ == "__main__":
#     main()

    #GDS_Connect()

################################
GDS_Connect()
input("Press Enter to continue. Connect Complete, Heartbeat next")
heartbeat()
#input("Press Enter to continue. Connect Complete, Logon next")

#print(HB_response)


#GDS_Disconnect()
#input("Press Enter to continue. Logon Complete, Add Samples next")

# GDS_Logon()
# input("Press Enter to continue. Logon Complete, Add Samples next")
# AddSamples()
# input("Press Enter to continue. Add Samples Complete, LastRemoteAddedSets next")
# LastRemoteAddedSets()
# input("Press Enter to continue. LastRemoteAddedSets Complete, AssignNextToAnalyze next")
# AssignNextToAnalyze()
# input("Press Enter to continue. AssignNextToAnalyz Complete, LoadSample next")
# LoadSample()
# input("Press Enter to continue. Analysis Complete")
# Analyze()

