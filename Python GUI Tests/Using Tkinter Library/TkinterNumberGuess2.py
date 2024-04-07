# Basic example of using Tkinter - Python 3 and above
# Useful links:
#    https://tkdocs.com/
#    https://docs.python.org/3/library/tk.html

from tkinter import *

# Create the Window and give it a title...
window = Tk()
window.title("Welcome to Number Guess")

# Set the Windows size...
window.geometry('900x150')

# Scale it up so we can see it better...
window.tk.call('tk', 'scaling', 3.0)  # scales the displayed text in the window

##########
#   Add our widgets...
##########

# Using grid() to location widgets
#    https://www.pythontutorial.net/tkinter/tkinter-grid/

# Create our label...
lbl = Label(window, text="Enter a number from 1 to 10: ")
lbl.grid(column=0, row=0) # can look at Grid.JPG to see what different indecies are

# Create the Spinbox to get the number guess...
txt_spin_value = 1
spinNumber = Spinbox(window, from_ = 1, to = 10, textvariable=txt_spin_value)
spinNumber.grid(column=1, row=0)

btnOk = Button(window, text="Ok")
btnOk.grid(column=0, row=2)

btnCancel = Button(window, text="Cancel")
btnCancel.grid(column=1, row=2)

window.mainloop()
