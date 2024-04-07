# Basic example of using Tkinter - Python 3 and above
# Useful links:
#    https://tkdocs.com/
#    https://docs.python.org/3/library/tk.html

# NOTES:
# - All buttons, text boxes, etc. are called widgets
# - Owner of all widgets are a window, (there is a heirarchy)


from tkinter import *

# Create the Window and give it a title...
window = Tk()
window.title("Welcome to Number Guess")

# Set the Windows size...
window.geometry('900x150') # pixel width x height 

# Scale it up so we can see it better...
window.tk.call('tk', 'scaling', 3.0)

window.mainloop()
