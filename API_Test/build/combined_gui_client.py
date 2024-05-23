from pathlib import Path
import socket
from tkinter import Tk, Canvas, Button, PhotoImage, Toplevel
import threading

# Setup socket communication
DESTINATION_IP = socket.gethostbyname(socket.gethostname())
DESTINATION_PORT = 6045
ENCODER = "utf-8"
BYTESIZE = 1024

# Establish Pathing
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\micah\OneDrive\MAE 156\Capstone Project\MAE-156-Capstone-Project\API_Test\build\assets\frame0")

# Create client socket and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DESTINATION_IP, DESTINATION_PORT))

# Function recieve data from server
def listen_for_server_messages():
    while True:
        try:
            data = client_socket.recv(BYTESIZE).decode(ENCODER)
            if data:
                # Example: Update calibration mode buttons based on data received
                if data == "Calibration Mode: ON":
                    # Ensuring GUI updates happen in the main thread
                    window.after(0, lambda: toggle_button_4_6(True))
                elif data == "Calibration Mode: OFF":
                    window.after(0, lambda: toggle_button_4_6(False))
        except Exception as e:
            print("Error receiving data:", e)
            break


# Function to send data to server
def send_data(data):
    """Send data to the server."""
    client_socket.send(data.encode(ENCODER))

# Function to build relative path to assets
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Main window setup
window = Tk()
window.title("API")
window.geometry("774x556")
window.configure(bg="#1F1F1F")

canvas = Canvas(window, bg="#1F1F1F", height=556, width=774, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)


########### Main GUI Setup ############

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    387.0,
    436.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    184.0,
    451.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    387.0,
    171.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    53.0,
    20.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    199.0,
    85.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    565.0,
    85.0,
    image=image_image_6
)

###### BUTTON FOR PLC CONNECT ######
#Load Images 
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png")) # Connect image
button_image_1_alt = PhotoImage(file=relative_to_assets("button_1_opposite.png"))  # Green Connected image
# function for button toggle between connect and connceted images
def toggle_button_1():
    if button_1.image_state:
        button_1.config(image=button_image_1_alt)
        button_1.image_state = False
    else:
        button_1.config(image=button_image_1)
        button_1.image_state = True
#Button object creation
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_1.place(
    x=568.0,
    y=75.0,
    width=90.0,
    height=21.0
)
button_1.image_state = True  # True for original image, False for alternate image
button_1.config(command=toggle_button_1) # Assign the toggle function to button command


image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    387.0,
    254.0,
    image=image_image_7
)

###### BUTTON FOR CORNERSTONE CONNECT ######
#Load Images 
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png")) # Connect image
button_image_2_alt = PhotoImage(file=relative_to_assets("button_2_opposite.png"))  # Green Connected image
# function for button toggle between connect and connceted images
def toggle_button_2():
    if button_2.image_state:
        button_2.config(image=button_image_2_alt)
        button_2.image_state = False
    else:
        button_2.config(image=button_image_2)
        button_2.image_state = True
#Button object creation
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_2.place(
    x=221.0,
    y=75.0,
    width=90.0,
    height=21.0
)
button_2.image_state = True  # True for original image, False for alternate image
button_2.config(command=toggle_button_2) # Assign the toggle function to button command

###### 8 AND 16 SPOKE BUTTONS (BUTTON 3 = 8 SPOKE, BUTTON 5 = 16 SPOKE) ######
button_image_3_light = PhotoImage(file=relative_to_assets("button_3_light.png"))
button_image_3_dark = PhotoImage(file=relative_to_assets("button_3_dark.png"))
button_image_5_light = PhotoImage(file=relative_to_assets("button_5_light.png"))
button_image_5_dark = PhotoImage(file=relative_to_assets("button_5_dark.png"))

# Define a function to toggle the images
def toggle_buttons_3_5(button):
    if button.image_state == "dark":
        if button == button_3:
            button_3.config(image=button_image_3_light)
            button_5.config(image=button_image_5_dark)
            button_3.image_state = "light"
            button_5.image_state = "dark"
        elif button == button_5:
            button_5.config(image=button_image_5_light)
            button_3.config(image=button_image_3_dark)
            button_5.image_state = "light"
            button_3.image_state = "dark"

# Setup buttons
button_3 = Button(window, image=button_image_3_light, borderwidth=0, highlightthickness=0, relief="flat")
button_3.place(x=372.0, y=151.0, width=90.0, height=41.0)
button_3.image_state = "light"  # Initial state
button_3.config(command=lambda: toggle_buttons_3_5(button_3))

button_5 = Button(window, image=button_image_5_dark, borderwidth=0, highlightthickness=0, relief="flat")
button_5.place(x=489.0, y=151.0, width=90.0, height=41.0)
button_5.image_state = "dark"  # Initial state
button_5.config(command=lambda: toggle_buttons_3_5(button_5))

###### CALIBRATION MODE BUTTONS (BUTTON 4 = ON, BUTTON 6 = OFF) ######
# Load button images
button_image_4_light = PhotoImage(file=relative_to_assets("button_4_light.png"))
button_image_4_dark = PhotoImage(file=relative_to_assets("button_4_dark.png"))
button_image_6_light = PhotoImage(file=relative_to_assets("button_6_light.png"))
button_image_6_dark = PhotoImage(file=relative_to_assets("button_6_dark.png"))

# Define a function to toggle the images
def toggle_buttons_4_6(button):
    if button.image_state == "dark":
        if button == button_4:
            button_4.config(image=button_image_4_light)
            button_6.config(image=button_image_6_dark)
            button_4.image_state = "light"
            button_6.image_state = "dark"
            Cal_status = "Calibration Mode: ON"
            send_data(Cal_status)
        elif button == button_6:
            button_6.config(image=button_image_6_light)
            button_4.config(image=button_image_4_dark)
            button_6.image_state = "light"
            button_4.image_state = "dark"
            Cal_status = "Calibration Mode: OFF"
            send_data(Cal_status)

# Setup buttons
button_4 = Button(window, image=button_image_4_dark, borderwidth=0, highlightthickness=0, relief="flat")
button_4.place(x=372.0, y=233.0, width=90.0, height=41.0)
button_4.image_state = "dark"  # Initial state
button_4.config(command=lambda: toggle_buttons_4_6(button_4))

button_6 = Button(window, image=button_image_6_light, borderwidth=0, highlightthickness=0, relief="flat")
button_6.place(x=489.0, y=233.0, width=90.0, height=41.0)
button_6.image_state = "light"  # Initial state
button_6.config(command=lambda: toggle_buttons_4_6(button_6))

###### DOORLOCK BUTTONS (BUTTON 8 = LOCKED, BUTTON 9 = UNLOCKED) ######
# Load button images
button_image_8_light = PhotoImage(file=relative_to_assets("button_8_light.png"))
button_image_8_dark = PhotoImage(file=relative_to_assets("button_8_dark.png"))
button_image_9_light = PhotoImage(file=relative_to_assets("button_9_light.png"))
button_image_9_dark = PhotoImage(file=relative_to_assets("button_9_dark.png"))

# Define a function to toggle the images
def toggle_buttons_8_9(button):
    if button.image_state == "dark":
        if button == button_8:
            button_8.config(image=button_image_8_light)
            button_9.config(image=button_image_9_dark)
            button_8.image_state = "light"
            button_9.image_state = "dark"
        elif button == button_9:
            button_9.config(image=button_image_9_light)
            button_8.config(image=button_image_8_dark)
            button_9.image_state = "light"
            button_8.image_state = "dark"

# Setup buttons
button_8 = Button(window, image=button_image_8_light, borderwidth=0, highlightthickness=0, relief="flat")
button_8.place(x=112.0, y=423.0, width=60.0, height=60.0)
button_8.image_state = "light"  # Initial state
button_8.config(command=lambda: toggle_buttons_8_9(button_8))

button_9 = Button(window, image=button_image_9_dark, borderwidth=0, highlightthickness=0, relief="flat")
button_9.place(x=198.0, y=423.0, width=60.0, height=54.0)
button_9.image_state = "dark"  # Initial state
button_9.config(command=lambda: toggle_buttons_8_9(button_9))


canvas.create_text(
    149.0,
    379.0,
    anchor="nw",
    text="Door lock:",
    fill="#FFFFFF",
    font=("RobotoRoman ExtraLight", 16 * -1)
)

canvas.create_text(
    545.0,
    381.0,
    anchor="nw",
    text="Current Spoke:",
    fill="#FFFFFF",
    font=("RobotoRoman ExtraLight", 16 * -1)
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    386.999969540484,
    320.0,
    image=image_image_8
)
# Button 7 - Analyze Button Setup and Press events
def button_7_pressed(button):
    Analyze_status = "Analyze Mode: ON"
    send_data(Analyze_status)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: button_7_pressed(button_7),
    relief="flat"
)
button_7.place(
    x=318.0,
    y=368.0,
    width=138.0,
    height=138.0
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    595.0,
    449.0,
    image=image_image_9
)


##################### ERROR GUI Function to call upon when vacuum error occurs #######################
#def open_error_window():
error_window = Toplevel(window)
error_window.title("API ERROR")
error_window.geometry("303x376")
error_window.configure(bg="#1F1F1F")

# Create a new canvas specifically for the error window
error_canvas = Canvas(error_window, bg="#1F1F1F", height=376, width=303, bd=0, highlightthickness=0, relief="ridge")
error_canvas.place(x=0, y=0)
error_canvas.create_rectangle(
    0.0,
    0.0,
    303.0,
    61.0,
    fill="#B95050",
    outline="")

image_image_1e = PhotoImage(
    file=relative_to_assets("image_1e.png"))
image_1e = error_canvas.create_image(
    151.0,
    103.0,
    image=image_image_1e
)

image_image_2e = PhotoImage(
    file=relative_to_assets("image_2e.png"))
image_2e = error_canvas.create_image(
    151.0,
    260.0,
    image=image_image_2e
)

error_canvas.create_text(
    70.0,
    19.0,
    anchor="nw",
    text="ERROR: Vacuum Failed",
    fill="#FFFFFF",
    font=("MontserratRoman Light", 18 * -1)
)

image_image_3e = PhotoImage(
    file=relative_to_assets("image_3e.png"))
image_3e = error_canvas.create_image(
    208.0,
    103.0,
    image=image_image_3e
)

error_canvas.create_text(
    205.0,
    96.0,
    anchor="nw",
    text="1\n",
    fill="#006262",
    font=("RobotoRoman Light", 12 * -1)
)

error_canvas.create_text(
    81.0,
    96.0,
    anchor="nw",
    text="Failure on Spoke: ",
    fill="#FFFFFF",
    font=("MontserratRoman Light", 12 * -1)
)

image_image_4e = PhotoImage(
    file=relative_to_assets("image_4e.png"))
image_4e = error_canvas.create_image(
    30.0,
    31.0,
    image=image_image_4e
)

error_canvas.create_text(
    29.0,
    146.0,
    anchor="nw",
    text="Do you wish to:",
    fill="#FFFFFF",
    font=("MontserratRoman Light", 12 * -1)
)

##### TRY AGAIN Button #####
button_image_1e = PhotoImage(
    file=relative_to_assets("button_1e.png"))
button_1e = Button(
    error_canvas,
    image=button_image_1e,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: send_data("try again"),
    relief="flat"
)
button_1e.place(
    x=100.0,
    y=192.0,
    width=102.0,
    height=30.0
)

#### SKIP SPOKE button ####
button_image_2e = PhotoImage(
    file=relative_to_assets("button_2e.png"))
button_2e = Button(
    error_canvas,
    image=button_image_2e,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: send_data("skip spoke"),
    relief="flat"
)
button_2e.place(
    x=100.0,
    y=246.0,
    width=102.0,
    height=30.0
)

#### ABORT Button ####
button_image_3e = PhotoImage(
    file=relative_to_assets("button_3e.png"))
button_3e = Button(
    error_canvas,
    image=button_image_3e,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: send_data("abort"),
    relief="flat"
)
button_3e.place(
    x=100.0,
    y=300.0,
    width=102.0,
    height=30.0
)

# Start the listener thread for receiving server messages
thread = threading.Thread(target=listen_for_server_messages)
thread.daemon = True  # Ensures the thread will exit when the main program does
thread.start()

# Define what happens when the window is about to be closed
def on_closing():
    try:
        client_socket.close()  # Attempt to close the socket connection
    except Exception as e:
        print("Error closing socket:", e)
    window.destroy()  # Destroy the main window to close the application

# Bind the close event to your closing function
window.protocol("WM_DELETE_WINDOW", on_closing)
window.resizable(False, False)
window.mainloop()
