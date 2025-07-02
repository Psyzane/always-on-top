from tkinter import *
from tkinter import ttk

# Create the main window
root = Tk()

# Create a frame widget
frm = ttk.Frame(root, padding=10)
frm.grid()

# Create a label widget
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)

# Create a button widget
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)


def runapp():
    print('Running...')
    # Start the main event loop
    root.mainloop()

if __name__ == '__main__':
    runapp()