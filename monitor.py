import automation_utils_master_console as Q
import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
from tkinter import ttk
import serial
import threading
import time
import sys
import numpy as np
import notebook_utils as notebook


# Q.arduino = serial.Serial('COM6', 9600)  # Change 'COM6' to your Arduino port
# time.sleep(2)  # Give some time for the connection to be established

Q.relay_states = {1: False, 2: False, 3: False, 4: False,
                  5: False, 6: False, 7: False, 8: False,
                  9: False, 10: False, 11: False, 12: False}

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):
        pass  # Required for file-like object interface


toggletime = int(500)

def save_textbox_input(textbox_no):
    global toggletime
    input_text = textbox_no.get("1.0", "end-1c")
    print("Delay time (in ms):", input_text)
    toggletime = int(input_text)


def toggle_off(relay_no):
    Q.arduino.write(f'1:{relay_no}:1\n'.encode('utf-8'))  # Send '0' to turn relay off




# Create the main window
root = tk.Tk()
root.title("Master Console")
root.configure(background='brown')
root.geometry("1000x300")


# First row - Monitors
monitor_frame = ttk.LabelFrame(root, text="Monitors",border=10)
monitor_frame.grid(row=0, column=0, padx=5, pady=5, columnspan=1, sticky="ew")
serial_ports = ['COM3', 'COM4', 'COM5']  # Change these as necessary
baud_rate = 9600
# # Create a frame for each monitor
# frames = [tk.Frame(root) for _ in range(3)]
# titles = ["Monitor 1", "Monitor 2", "Monitor 3"]


# Create serial connections and text widgets
serial_connections = []
textboxes = []
threads = []


    
titles = ["Monitor 1", "Monitor 2", "Monitor 3"]
for i in range(3):
    iteration=0
    label = tk.Label(monitor_frame, text=titles[i])
    label.grid(row=0, column=i, padx=5, pady=5)
    monitor_frame.grid(row = 0, column = i,  padx=10, pady=10)
    textbox = scrolledtext.ScrolledText(monitor_frame, width=30, height=5, wrap=tk.WORD)
    textbox.grid(row = 0, column = i,  padx=10, pady=10)
    textboxes.append(textbox)
    ser = Q.create_serial_connection(serial_ports[i], baud_rate)
    
    if ser:
        count=0
        count +=1
        serial_connections.append(ser)
        thread = threading.Thread(target=Q.read_from_serial, args=(ser, textbox), daemon=True)
        threads.append(thread)
        threads.append(" \n ufbnidfn")
        thread.start()  #might create a memory problem
        # values=notebook.read_from_serial(ser)
        # if count==5:

        #     threads.append('saved ',thread)
        #     np.savetxt('E:\QuMaC\Codes\COMread',values)
        #     count=0
        #     time.sleep(2)
    


# Start the Tkinter main loop
root.mainloop()

    

# Close the serial ports when the program is closed
for ser in serial_connections:
    ser.close()
