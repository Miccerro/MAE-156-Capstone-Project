#TCP Client Side, PC 
import socket
import xml.etree.ElementTree as ET
import time


#Define constants
DESTINATION_IP = socket.gethostbyname(socket.gethostname())
DESTINATION_PORT = 12345
ENCODER = "utf-8"
BYTESIZE = 1024

#Create client socket and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DESTINATION_IP, DESTINATION_PORT))

#Send/Recieve messages from server
while True:
    #Recieve information from the server
    message = client_socket.recv(BYTESIZE).decode(ENCODER)
    print(f"\n{message}")

    # #Quit if the connected server wants to quit, else keep sending messages
    # if message == "quit":
    #     client_socket.send("quit".encode(ENCODER))
    #     print("\nEnding the Chat (Client Side)... Goodbye!!")
    #     break
    # else:
    #         print(f"\n{message}")
    #         message = input("Message: ")
    #         if message == "Command":
    #             message = "<ExecuteSequence Sequence='Ream Anode' />"
    #             client_socket.send(message.encode(ENCODER))
    #         else:
    #             client_socket.send(message.encode(ENCODER))

    #Examples of possible XML messages to send to GDS:
    xml_message1 = "<ExecuteSequence Sequence='Prep Sample' />"
    xml_message2 = "<ExecuteSequence Sequence='Load Sample' />"
    xml_message3 = "<ExecuteSequence Sequence='Load Sample Step 1' />"
    xml_message4 = "<ExecuteSequence Sequence='Load Sample Step 2' />"
    xml_message5 = "<ExecuteSequence Sequence='Load Sample Step 3' />"
    xml_message6 = "<ExecuteSequence Sequence='Ream Anode' />"



    #Assume we send over commands (will figure out later what order they go)
    #Send over ream 
    client_socket.send(xml_message6.encode(ENCODER))

    #OUR LISTINE TO ACT AFTER RECIEVING THIS MESSAGE
    #"<Sequence Name='Ream Anode' Running='true' LastReturnResult='' />"
    #OR
    #"<Sequence Name='Ream Anode' Running='true' LastReturnResult='' />"

    xml_message = client_socket.recv(BYTESIZE).decode(ENCODER)
    print("Received XML message from GDS:", xml_message)

    #parse XML message:
    root = ET.fromstring(xml_message)
    running = root.get('Running')
    print("Running:", running)

    # Wait until 'Running' is 'complete'
    while running != 'complete':
        xml_message = client_socket.recv(BYTESIZE).decode(ENCODER)
        root = ET.fromstring(xml_message)
        running = root.get('Running')
        print("Running:", running)
        print("This proves that we can parse xml messages. We can place a command here to execute something, like the next step would be to move the motors away from reamin area")

#This is a simple example of pasring XML messages. Will need to start learning the order
#We can already start psuedocode to layout how we will respond to certain messages. Need aspecific step by step





#Close Client Socket
client_socket.close()


