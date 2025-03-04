import tkinter as tk
from tkinter import ttk
# https://www.activestate.com/resources/quick-reads/how-to-position-widgets-in-tkinter/

root = tk.Tk()

# pack

# vertical
# root.geometry("300x300")
# test = tk.Label(root, text="Red", bg="red", fg="white")
# test.pack(side=tk.BOTTOM)
# test = tk.Label(root, text="Green", bg="green", fg="white")
# test.pack(side=tk.BOTTOM)
# test = tk.Label(root, text="Purple", bg="purple", fg="white")
# test.pack(side=tk.BOTTOM)

# side-by-side
# root.geometry("300x300")
# test = tk.Label(root, text="red", bg="red", fg="white")
# test.pack(padx=5, pady=15, side=tk.LEFT)
# test = tk.Label(root, text="green", bg="green", fg="white")
# test.pack(padx=5, pady=20, side=tk.LEFT)
# test = tk.Label(root, text="purple", bg="purple", fg="white")
# test.pack(padx=5, pady=20, side=tk.LEFT)


# place

# root.geometry('250x200+250+200')
# tk.Label(root, text="Position 1 : x=0, y=0", bg="#FFFF00", fg="black").place(x=5, y=0)
# tk.Label(root, text="Position 2 : x=50, y=40", bg="#3300CC", fg="white").place(x=50, y=40)
# tk.Label(root, text="Position 3 : x=75, y=80", bg="#FF0099", fg="white").place(x=75, y=80)


# grid
root.geometry("300x300")
tk.Label(text="Position 1", width=10).grid(row=0, column=0)
tk.Label(text="Position 2", width=10).grid(row=0, column=1)
tk.Label(text="Position 3", width=10).grid(row=1, column=0)
tk.Label(text="Position 4", width=10).grid(row=1, column=1)


# ttk

# Style() padding adds pixels inside the Button. The widget’s position is not changed.
# ttk.Style().configure("TButton", padding=5, relief="flat")
# button1 = ttk.Button(text="Button Example")

# pack() padding adds pixels outside the TButton. The widget’s position is changed.
# button1.pack(side = 'bottom', padx='x_coordinate', pady='y_coordinate')

root.mainloop()