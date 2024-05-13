# #This is to test the use of the main.py file
# #Import needed functions from other files:
# import subprocess
# from transitions import Machine

# GUI_path = r'C:\Users\emont\OneDrive\Desktop\MAE156A\MAE-156-Capstone-Project\Python GUI Tests 2\build\gui-4-18.py'

# #USED FOR DEBUGGING
# result = subprocess.run(["python", GUI_path])

# # Run the GUI subprocess and capture the output (USED TO AVOID SYTAX ERROR)
# result = subprocess.run(["python", GUI_path], capture_output=True, text=True)

# # Get the captured output
# output = result.stdout

# # Print the output
# print(output)




import subprocess
from transitions import Machine

class MyStateMachine:
    states = ['CALIBRATION', 'IDLE']

    def __init__(self):
        self.machine = Machine(model=self, states=MyStateMachine.states, initial='IDLE')
        self.machine.add_transition(trigger='button_4_pressed', source='*', dest='CALIBRATION', after='start_calibration')
        self.machine.add_transition(trigger='button_6_pressed', source='*', dest='IDLE', after='stop_calibration')

    def start_calibration(self):
        print("Starting calibration...")
        # Add your calibration logic here

    def stop_calibration(self):
        print("Stopping calibration...")
        # Add your idle logic here

def main():
    # GUI path
    GUI_path = r'C:\Users\emont\OneDrive\Desktop\MAE156A\MAE-156-Capstone-Project\Python GUI Tests 2\build\gui-4-18.py'
    
    # Create an instance of the state machine
    state_machine = MyStateMachine()

    # Run the GUI subprocess asynchronously
    gui_process = subprocess.Popen(["python", GUI_path])

    # Prompt for user input for button press simulation
    button_press = input("Enter button press (BUTTON4 or BUTTON6): ")

    # Trigger transitions based on button presses
    if button_press == "BUTTON4":
        state_machine.button_4_pressed()
        print("in1")
    elif button_press == "BUTTON6":
        state_machine.button_6_pressed()
        print("in2")

if __name__ == "__main__":
    main()





##Atempt to Connect to PLC 
# from transitions import Machine
# import socket
# result = subprocess.run(["python", script_path], capture_output=True, text=True)
# calibration_mode = result.stdout.strip()

# # PLC IP address and port
# PLC_IP = "192.168.1.177"  # Replace with your PLC's IP address
# PLC_PORT = 8888  # Port number of the PLC server

# # Create a TCP/IP socket
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("Called successfully")
# try:
#     # Connect to the PLC server
#     client_socket.connect((PLC_IP, PLC_PORT))
#     print("Connected to PLC successfully")

#     # Send the color change message
#     color_values = "255,255,255"  # White color (R:255, G:255, B:255)
#     client_socket.sendall(color_values.encode())

#     #print("Color changed to white successfully.")

# except Exception as e:
#     print("Error:", e)

# finally:
#     # Close the socket
#     client_socket.close()


