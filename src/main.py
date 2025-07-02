import tkinter as tk
from tkinter import ttk
from util import *

# Create the main window
root = tk.Tk(className="Tappy")
root.geometry('600x400')

# Create a frame widget
frm = ttk.Frame(root, padding=10)
frm.grid()

# Create a label widget
ttk.Label(frm, text="Active Windows", background='#fff', font=('Arial', 14)).grid(column=0, row=0)


options = ttk.Frame(frm, padding=10, width=600)
options.grid(column=0, row=1)

for index, win in enumerate(get_active_windows_titles()):
    ttk.Button(options, text=win, command=lambda w=win: toggle_topmost_by_title(w)).pack(fill="x", expand=1)

ttk.Button(options, text='Reset', command=remove_always_on_top_from_all_windows).pack(fill="x", expand=1)


# Create a button widget
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=2)


def runapp():
    print("Running...")
    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    runapp()
