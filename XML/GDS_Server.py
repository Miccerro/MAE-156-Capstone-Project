#TCP Server Side, GDS (via corenrstone)
import socket
import xml.etree.ElementTree as ET
import time

# Define constants
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
ENCODER = "utf-8"
BYTESIZE = 1024

#Create server socket, bind it to ip/port, and listen
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

#Accept any incoming connection and let them know they are connected
print("Server is running... \n")
client_socket, client_address = server_socket.accept()
client_socket.send("You are connected to the server...\n".encode(ENCODER))

#Infinite loop to Send/Recieve messages as server
while True:
    #Recieve information from the client
    message = client_socket.recv(BYTESIZE).decode(ENCODER)

    # #Quit if client socket wants to quit, else display the message
    # if message == "quit":
    #     client_socket.send("quit".encode(ENCODER))
    #     print("\n Ending the chat (Server side)... Goodbye!!")
    #     break
    # else:
    #     print(f"\n{message}")
    #     message = input("Message: ")
    #     client_socket.send(message.encode(ENCODER))

    #Examples of possible XML messages that the GDS will send (not 100%) (may be another format)
    xml_message1 = '<Sequence Name="Prep Sample" Running="false" LastReturnResult="" />'
    xml_message2 = '<Sequence Name="Load Sample" Running="false" LastReturnResult="" />'
    xml_message3 = '<Sequence Name="Load Sample Step 1" Running="false" LastReturnResult="Error: pressure evacuation timeout" />'
    xml_message4 = '<Sequence Name="Load Sample Step 2" Running="false" LastReturnResult="" />'
    xml_message4 = '<Sequence Name="Load Sample Step 3" Running="false" LastReturnResult="" />'
    xml_message5 = '<Sequence Name="Ream Anode" Running="false" LastReturnResult="" />'
    
    #Lets imagine the GDS takes a while to execute the command
   #USED FOR REFRENCE: NOTE: <ExecuteSequence Sequence='Ream Anode' />  AT THIS POINBT WE GET THIS XML COMMAND
    
    
    
    root = ET.fromstring(message)
    # Read the value of the 'Sequence' attribute
    sequence_value = root.get('Sequence')
    if root.tag == "ExecuteSequence":
        sequence_value = root.get('Sequence')
        print("Received ExecuteSequence:", sequence_value)
        response = "<Sequence Name='Ream Anode' Running='true' LastReturnResult='' />"
        client_socket.send(response.encode())

        # Wait for 4 seconds
        time.sleep(4)
        # Send the response
        response = "<Sequence Name='Ream Anode' Running='complete' LastReturnResult='' />"
        client_socket.send(response.encode())
        time.sleep(1000)
    else:
            print("Received unknown XML message:", xml_string)



# Close the socket
server_socket.close()
