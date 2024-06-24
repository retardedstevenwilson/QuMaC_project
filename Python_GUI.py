import tkinter as tk
from tkinter import messagebox

def on_button_click():
    messagebox.showinfo("Information", "Hello, World!")

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter GUI")

# Create a label
label = tk.Label(root, text="Welcome to Tkinter!")
label.pack(pady=10)

# Create a button
button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
