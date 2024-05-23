
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\micah\OneDrive\MAE 156\Capstone Project\MAE-156-Capstone-Project\API_Test\build\error assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("API ERROR")

window.geometry("303x376")
window.configure(bg = "#1F1F1F")


canvas = Canvas(
    window,
    bg = "#1F1F1F",
    height = 376,
    width = 303,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    303.0,
    61.0,
    fill="#B95050",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1e.png"))
image_1 = canvas.create_image(
    151.0,
    103.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2e.png"))
image_2 = canvas.create_image(
    151.0,
    260.0,
    image=image_image_2
)

canvas.create_text(
    70.0,
    19.0,
    anchor="nw",
    text="ERROR: Vacuum Failed",
    fill="#FFFFFF",
    font=("MontserratRoman Light", 18 * -1)
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3e.png"))
image_3 = canvas.create_image(
    208.0,
    103.0,
    image=image_image_3
)

canvas.create_text(
    205.0,
    96.0,
    anchor="nw",
    text="1\n",
    fill="#006262",
    font=("RobotoRoman Light", 12 * -1)
)

canvas.create_text(
    81.0,
    96.0,
    anchor="nw",
    text="Failure on Spoke: ",
    fill="#FFFFFF",
    font=("MontserratRoman Light", 12 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4e.png"))
image_4 = canvas.create_image(
    30.0,
    31.0,
    image=image_image_4
)

canvas.create_text(
    29.0,
    146.0,
    anchor="nw",
    text="Do you wish to:",
    fill="#FFFFFF",
    font=("MontserratRoman Light", 12 * -1)
)

##### TRY AGAIN Button #####
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1e.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=100.0,
    y=192.0,
    width=102.0,
    height=30.0
)

#### SKIP SPOKE button ####
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2e.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=100.0,
    y=246.0,
    width=102.0,
    height=30.0
)

#### ABORT Button ####
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3e.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=100.0,
    y=300.0,
    width=102.0,
    height=30.0
)
window.resizable(False, False)
window.mainloop()
