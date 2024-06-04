from pathlib import Path
import socket
from tkinter import Tk, Canvas, Button, PhotoImage, Toplevel, Label
import threading

# Setup socket communication
DESTINATION_IP = socket.gethostbyname(socket.gethostname())
DESTINATION_PORT = 6045
ENCODER = "utf-8"
BYTESIZE = 1024

# Establish Pathing
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\micah\OneDrive\MAE 156\Capstone Project\MAE-156-Capstone-Project\API_Test\API_build\assets\frame0")
# Create client socket and connect to main.py server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DESTINATION_IP, DESTINATION_PORT))

def relative_to_assets(path: str) -> Path:
    full_path = ASSETS_PATH / Path(path)
    print(f"Full path for {path}: {full_path}")
    return full_path

# Function that recieves data from main.py server. It is set to recieve four different messages that toggle the images for the calibration mode buttons
# and the PLC connect and Cornerstone connect buttons
def listen_for_server_messages():
    while True:
        try:
            data = client_socket.recv(BYTESIZE).decode(ENCODER)
            if data:
                if data == "Calibration Mode: ON":
                    window.after(0, lambda: toggle_buttons_4_6(True, from_server=True))
                elif data == "Calibration Mode: OFF":
                    window.after(0, lambda: toggle_buttons_4_6(False, from_server=True))
                elif data == "PLC Connected":
                    window.after(0, toggle_button_1)
                elif data == "Cornerstone Connected":
                    window.after(0, toggle_button_2)
                elif data.isdigit():
                    window.after(0, lambda: spoke_label.config(text=data))
                elif data == 'Vacuum Error':
                    print("Vacuum Error has occurred opening Error GUI")
                    window.after(0, open_error_window)  # Opens the error GUI
        except Exception as e:
            print("Error receiving data:", e)
            break

# def listen_for_server_messages():
#     while True:
#         try:
#             data = client_socket.recv(BYTESIZE).decode(ENCODER)
#             if data:
#                 # Example: Update calibration mode buttons based on data received
#                 if data == "Calibration Mode: ON":
#                     # Ensuring GUI updates happen in the main thread
#                     window.after(0, lambda: toggle_buttons_4_6(True))
#                 elif data == "Calibration Mode: OFF":
#                     window.after(0, lambda: toggle_buttons_4_6(False))
#         except Exception as e:
#             print("Error receiving data:", e)
#             break


# Function to sends string data to the main.py server using utf-8 encoding
def send_data(data):
    """Send data to the server."""
    client_socket.send(data.encode(ENCODER))

# Function to build relative path to assets
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


if __name__ == "__main__":
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

    # This function sends a message to the server when the user presses button 1
    def request_plc_connection():
        send_data("connect plc request")

    # This functions toggles the button state only when called by the server message handler
    def toggle_button_1():
        button_1.config(image=button_image_1_alt if button_1.image_state else button_image_1)
        button_1.image_state = not button_1.image_state

    # def toggle_button_1(from_server=False):
    #     if from_server or button_1.image_state:
    #         new_state = not button_1.image_state
    #         button_1.config(image=button_image_1_alt if button_1.image_state else button_image_1)
    #         button_1.image_state = not button_1.image_state
    #         print(f"Button 1 toggled to {'connected' if new_state else 'disconnected'} by {'server' if from_server else 'user'}")
    # def toggle_button_1():
    #     if button_1.image_state:
    #         button_1.config(image=button_image_1_alt)
    #         button_1.image_state = False
    #     else:
    #         button_1.config(image=button_image_1)
    #         button_1.image_state = True

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
    button_1.config(command=request_plc_connection) # sends plc connection request to main.py upon button press


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

    # This function sends a message to the main.py server when the user presses button 2
    def request_cornerstone_connection():
        send_data("connect cornerstone request")

    # This functions toggles the button state only when called by the server message handler
    def toggle_button_2():
        button_2.config(image=button_image_2_alt if button_2.image_state else button_image_2)
        button_2.image_state = not button_2.image_state

    # def toggle_button_2(from_server=False):
    #     if from_server or button_2.image_state:
    #         button_2.config(image=button_image_2_alt if button_2.image_state else button_image_2)
    #         button_2.image_state = not button_2.image_state
    # def toggle_button_2():
    #     if button_2.image_state:
    #         button_2.config(image=button_image_2_alt)
    #         button_2.image_state = False
    #     else:
    #         button_2.config(image=button_image_2)
    #         button_2.image_state = True
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
    button_2.config(command=request_cornerstone_connection) # sends cornerstone connection request to main.py upon button press

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
                WW_select = "8-Spoke Wagon Wheel Selected"
                send_data(WW_select)
            elif button == button_5:
                button_5.config(image=button_image_5_light)
                button_3.config(image=button_image_3_dark)
                button_5.image_state = "light"
                button_3.image_state = "dark"
                WW_select = "16-Spoke Wagon Wheel Selected"
                send_data(WW_select)

    # Setup buttons - Default selection is 8-spoke wagon wheel
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
    def toggle_buttons_4_6(force_state=None, from_server=False):
        if from_server:
            # Force the state based on the data received from the server
            if force_state is not None:
                button_4.config(image=button_image_4_light if force_state else button_image_4_dark)
                button_6.config(image=button_image_6_dark if force_state else button_image_6_light)
                button_4.image_state = "light" if force_state else "dark"
                button_6.image_state = "dark" if force_state else "light"
        else:
            # Toggle based on current state for manual interactions
            if button_4.image_state == "dark":
                button_4.config(image=button_image_4_light)
                button_6.config(image=button_image_6_dark)
                button_4.image_state = "light"
                button_6.image_state = "dark"
                send_data("calibration on") # message sent to main.py server upon on button click
            else:
                button_4.config(image=button_image_4_dark)
                button_6.config(image=button_image_6_light)
                button_4.image_state = "dark"
                button_6.image_state = "light"
                send_data("calibration off") # message sent to main.py server upon off button click

    # Setup buttons
    button_4 = Button(window, image=button_image_4_dark, borderwidth=0, highlightthickness=0, relief="flat")
    button_4.place(x=372.0, y=233.0, width=90.0, height=41.0)
    button_4.image_state = "dark"  # Initial state
    button_4.config(command=lambda: toggle_buttons_4_6(from_server=False))

    button_6 = Button(window, image=button_image_6_light, borderwidth=0, highlightthickness=0, relief="flat")
    button_6.place(x=489.0, y=233.0, width=90.0, height=41.0)
    button_6.image_state = "light"  # Initial state
    button_6.config(command=lambda: toggle_buttons_4_6(from_server=False))

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
        Analyze_status = "Start Analysis Process" # when analysis button pressed, gui.py sends over this message to main.py server
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

    # image_image_9 = PhotoImage(
    #     file=relative_to_assets("image_9.png"))
    # image_9 = canvas.create_image(
    #     595.0,
    #     449.0,
    #     image=image_image_9
    # )

    ######## Label widget for the current spoke ########
    spoke_label = Label(
        window, 
        text="0", 
        font=("RobotoRoman ExtraLight", 16), 
        bg="#1F1F1F", 
        fg="#FFFFFF"
    )
    spoke_label.place(x=586.0, y=429.0)


    ##################### ERROR GUI Function to call upon when vacuum error occurs #######################
    def open_error_window():
        if hasattr(open_error_window, 'window') and open_error_window.window.winfo_exists():
            return  # Error window is already open

        open_error_window.window = Toplevel(window)
        open_error_window.window.title("API ERROR")
        open_error_window.window.geometry("303x376")
        open_error_window.window.configure(bg="#1F1F1F")

        def close_error_window():
            open_error_window.window.destroy()

        def handle_error_response(command):
            print(f"Sending {command} to the server...")
            send_data(command)
            close_error_window()  # Close the error window after sending command

        # Create a new canvas specifically for the error window
        error_canvas = Canvas(open_error_window.window, bg="#1F1F1F", height=376, width=303, bd=0, highlightthickness=0, relief="ridge")
        error_canvas.place(x=0, y=0)
        error_canvas.create_rectangle(
            0.0,
            0.0,
            303.0,
            61.0,
            fill="#B95050",
            outline="")

        try:
            print("Loading images for error window")
            open_error_window.image_image_1e = PhotoImage(file=relative_to_assets("image_1e.png"))
            open_error_window.image_image_2e = PhotoImage(file=relative_to_assets("image_2e.png"))
            open_error_window.image_image_3e = PhotoImage(file=relative_to_assets("image_3e.png"))
            open_error_window.image_image_4e = PhotoImage(file=relative_to_assets("image_4e.png"))

            open_error_window.button_image_1e = PhotoImage(file=relative_to_assets("button_1e.png"))
            open_error_window.button_image_2e = PhotoImage(file=relative_to_assets("button_2e.png"))
            open_error_window.button_image_3e = PhotoImage(file=relative_to_assets("button_3e.png"))

            print("Images loaded successfully")
        except Exception as e:
            print(f"Error loading images: {e}")

        error_canvas.create_image(151.0, 103.0, image=open_error_window.image_image_1e)
        error_canvas.create_image(151.0, 260.0, image=open_error_window.image_image_2e)

        error_canvas.create_text(
            70.0,
            19.0,
            anchor="nw",
            text="ERROR: Vacuum Failed",
            fill="#FFFFFF",
            font=("MontserratRoman Light", 18 * -1)
        )

        error_canvas.create_image(208.0, 103.0, image=open_error_window.image_image_3e)

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

        error_canvas.create_image(30.0, 31.0, image=open_error_window.image_image_4e)

        error_canvas.create_text(
            29.0,
            146.0,
            anchor="nw",
            text="Do you wish to:",
            fill="#FFFFFF",
            font=("MontserratRoman Light", 12 * -1)
        )

        ##### TRY AGAIN Button #####
        button_1e = Button(
            open_error_window.window,
            image=open_error_window.button_image_1e,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: handle_error_response("try again"),
            relief="flat"
        )
        button_1e.place(
            x=100.0,
            y=192.0,
            width=102.0,
            height=30.0
        )

        #### SKIP SPOKE button ####
        button_2e = Button(
            open_error_window.window,
            image=open_error_window.button_image_2e,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: handle_error_response("skip spoke"),
            relief="flat"
        )
        button_2e.place(
            x=100.0,
            y=246.0,
            width=102.0,
            height=30.0
        )

        #### ABORT Button ####
        button_3e = Button(
            open_error_window.window,
            image=open_error_window.button_image_3e,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: handle_error_response("abort"),
            relief="flat"
        )
        button_3e.place(
            x=100.0,
            y=300.0,
            width=102.0,
            height=30.0
        )



    # def open_error_window():
    #     if hasattr(open_error_window, 'window') and open_error_window.window.winfo_exists():
    #         return  # Error window is already open

    #     open_error_window.window = Toplevel(window)
    #     open_error_window.window.title("API ERROR")
    #     open_error_window.window.geometry("303x376")
    #     open_error_window.window.configure(bg="#1F1F1F")

    #     def close_error_window():
    #         open_error_window.window.destroy()

    #     def handle_error_response(command):
    #         print(f"Sending {command} to the server...")
    #         send_data(command)
    #         close_error_window()  # Close the error window after sending command

    #     # Create a new canvas specifically for the error window
    #     error_canvas = Canvas(open_error_window.window, bg="#1F1F1F", height=376, width=303, bd=0, highlightthickness=0, relief="ridge")
    #     error_canvas.place(x=0, y=0)
    #     error_canvas.create_rectangle(
    #         0.0,
    #         0.0,
    #         303.0,
    #         61.0,
    #         fill="#B95050",
    #         outline="")

    #     image_image_1e = PhotoImage(
    #         file=relative_to_assets("image_1e.png"))
    #     image_1e = error_canvas.create_image(
    #         151.0,
    #         103.0,
    #         image=image_image_1e
    #     )

    #     image_image_2e = PhotoImage(
    #         file=relative_to_assets("image_2e.png"))
    #     image_2e = error_canvas.create_image(
    #         151.0,
    #         260.0,
    #         image=image_image_2e
    #     )

    #     error_canvas.create_text(
    #         70.0,
    #         19.0,
    #         anchor="nw",
    #         text="ERROR: Vacuum Failed",
    #         fill="#FFFFFF",
    #         font=("MontserratRoman Light", 18 * -1)
    #     )

    #     image_image_3e = PhotoImage(
    #         file=relative_to_assets("image_3e.png"))
    #     image_3e = error_canvas.create_image(
    #         208.0,
    #         103.0,
    #         image=image_image_3e
    #     )

    #     error_canvas.create_text(
    #         205.0,
    #         96.0,
    #         anchor="nw",
    #         text="1\n",
    #         fill="#006262",
    #         font=("RobotoRoman Light", 12 * -1)
    #     )

    #     error_canvas.create_text(
    #         81.0,
    #         96.0,
    #         anchor="nw",
    #         text="Failure on Spoke: ",
    #         fill="#FFFFFF",
    #         font=("MontserratRoman Light", 12 * -1)
    #     )

    #     image_image_4e = PhotoImage(
    #         file=relative_to_assets("image_4e.png"))
    #     image_4e = error_canvas.create_image(
    #         30.0,
    #         31.0,
    #         image=image_image_4e
    #     )

    #     error_canvas.create_text(
    #         29.0,
    #         146.0,
    #         anchor="nw",
    #         text="Do you wish to:",
    #         fill="#FFFFFF",
    #         font=("MontserratRoman Light", 12 * -1)
    #     )

    #     ##### TRY AGAIN Button #####
    #     button_image_1e = PhotoImage(
    #         file=relative_to_assets("button_1e.png"))
    #     button_1e = Button(
    #         open_error_window.window,
    #         image=button_image_1e,
    #         borderwidth=0,
    #         highlightthickness=0,
    #         command=lambda: handle_error_response("try again"),
    #         relief="flat"
    #     )
    #     button_1e.place(
    #         x=100.0,
    #         y=192.0,
    #         width=102.0,
    #         height=30.0
    #     )

    #     #### SKIP SPOKE button ####
    #     button_image_2e = PhotoImage(
    #         file=relative_to_assets("button_2e.png"))
    #     button_2e = Button(
    #         open_error_window.window,
    #         image=button_image_2e,
    #         borderwidth=0,
    #         highlightthickness=0,
    #         command=lambda: handle_error_response("skip spoke"),
    #         relief="flat"
    #     )
    #     button_2e.place(
    #         x=100.0,
    #         y=246.0,
    #         width=102.0,
    #         height=30.0
    #     )

    #     #### ABORT Button ####
    #     button_image_3e = PhotoImage(
    #         file=relative_to_assets("button_3e.png"))
    #     button_3e = Button(
    #         open_error_window.window,
    #         image=button_image_3e,
    #         borderwidth=0,
    #         highlightthickness=0,
    #         command=lambda: handle_error_response("abort"),
    #         relief="flat",
    #     )
    #     button_3e.place(
    #         x=100.0,
    #         y=300.0,
    #         width=102.0,
    #         height=30.0
    #     )

### DEBUGGING ERROR GUI ###
    # def open_error_window():
    #     if hasattr(open_error_window, 'window') and open_error_window.window.winfo_exists():
    #         print("Error window already open")
    #         return  # Error window is already open

    #     open_error_window.window = Toplevel(window)
    #     open_error_window.window.title("API ERROR")
    #     open_error_window.window.geometry("303x376")
    #     open_error_window.window.configure(bg="#1F1F1F")

    #     def close_error_window():
    #         print("Closing error window")
    #         open_error_window.window.destroy()

    #     def handle_error_response(command):
    #         print(f"Sending {command} to the server...")
    #         send_data(command)
    #         close_error_window()  # Close the error window after sending command

    #     # Create a new canvas specifically for the error window
    #     error_canvas = Canvas(open_error_window.window, bg="#1F1F1F", height=376, width=303, bd=0, highlightthickness=0, relief="ridge")
    #     error_canvas.place(x=0, y=0)
    #     error_canvas.create_rectangle(
    #         0.0,
    #         0.0,
    #         303.0,
    #         61.0,
    #         fill="#B95050",
    #         outline="")

    #     print("Creating images for error window")
    #     image_image_1e = PhotoImage(
    #         file=relative_to_assets("image_1e.png"))
    #     image_1e = error_canvas.create_image(
    #         151.0,
    #         103.0,
    #         image=image_image_1e
    #     )

    #     image_image_2e = PhotoImage(
    #         file=relative_to_assets("image_2e.png"))
    #     image_2e = error_canvas.create_image(
    #         151.0,
    #         260.0,
    #         image=image_image_2e
    #     )

    #     error_canvas.create_text(
    #         70.0,
    #         19.0,
    #         anchor="nw",
    #         text="ERROR: Vacuum Failed",
    #         fill="#FFFFFF",
    #         font=("MontserratRoman Light", 18 * -1)
    #     )

    #     image_image_3e = PhotoImage(
    #         file=relative_to_assets("image_3e.png"))
    #     image_3e = error_canvas.create_image(
    #         208.0,
    #         103.0,
    #         image=image_image_3e
    #     )

    #     error_canvas.create_text(
    #         205.0,
    #         96.0,
    #         anchor="nw",
    #         text="1\n",
    #         fill="#006262",
    #         font=("RobotoRoman Light", 12 * -1)
    #     )

    #     error_canvas.create_text(
    #         81.0,
    #         96.0,
    #         anchor="nw",
    #         text="Failure on Spoke: ",
    #         fill="#FFFFFF",
    #         font=("MontserratRoman Light", 12 * -1)
    #     )

    #     image_image_4e = PhotoImage(
    #         file=relative_to_assets("image_4e.png"))
    #     image_4e = error_canvas.create_image(
    #         30.0,
    #         31.0,
    #         image=image_image_4e
    #     )

    #     error_canvas.create_text(
    #         29.0,
    #         146.0,
    #         anchor="nw",
    #         text="Do you wish to:",
    #         fill="#FFFFFF",
    #         font=("MontserratRoman Light", 12 * -1)
    #     )

    #     print("Creating buttons for error window")
    #     ##### TRY AGAIN Button #####
    #     button_1e = Button(
    #         open_error_window.window,
    #         text="Try Again",
    #         borderwidth=0,
    #         highlightthickness=0,
    #         command=lambda: handle_error_response("try again"),
    #         relief="flat",
    #         bg="#C3C3C3",
    #         fg="white"
    #     )
    #     button_1e.place(
    #         x=100.0,
    #         y=192.0,
    #         width=102.0,
    #         height=30.0
    #     )
    #     print("Button 'Try Again' created and placed")

    #     #### SKIP SPOKE button ####
    #     button_2e = Button(
    #         open_error_window.window,
    #         text="Skip Spoke",
    #         borderwidth=0,
    #         highlightthickness=0,
    #         command=lambda: handle_error_response("skip spoke"),
    #         relief="flat",
    #         bg="#C3C3C3",
    #         fg="black"
    #     )
    #     button_2e.place(
    #         x=100.0,
    #         y=246.0,
    #         width=102.0,
    #         height=30.0
    #     )
    #     print("Button 'Skip Spoke' created and placed")

    #     #### ABORT Button ####
    #     button_3e = Button(
    #         open_error_window.window,
    #         text="Abort",
    #         borderwidth=0,
    #         highlightthickness=0,
    #         command=lambda: handle_error_response("abort"),
    #         relief="flat",
    #         bg="#C3C3C3",
    #         fg="white"
    #     )
    #     button_3e.place(
    #         x=100.0,
    #         y=300.0,
    #         width=102.0,
    #         height=30.0
    #     )
    #     print("Button 'Abort' created and placed")



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
