import tkinter as tk
from tkinter import ttk
import threading
import time
import sys
import os
from console_2_hardconnections import *

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):
        pass  # Required for file-like object interface
    


# Create the main window
root = tk.Tk()
root.title("Master Console")
root.configure(background='brown')
root.geometry("600x400")

# First row - Monitors
monitor_frame = ttk.LabelFrame(root, text="Monitors", border=10)
monitor_frame.grid(row=0, column=0, padx=5, pady=5, columnspan=1, sticky="ew")
baud_rate = 9600

# GPT: explanation - Create individual labels and textboxes for monitors
buffervolume_label = tk.Label(monitor_frame, text="Buffer Volume")
buffervolume_label.grid(row=0, column=0, padx=5, pady=5)
buffervolume_textbox = tk.Text(monitor_frame, width=30, height=1, wrap=tk.WORD)
buffervolume_textbox.grid(row=1, column=0, padx=10, pady=10)

loadlock_label = tk.Label(monitor_frame, text="Loadlock")
loadlock_label.grid(row=0, column=1, padx=5, pady=5)
loadlock_textbox = tk.Text(monitor_frame, width=30, height=1, wrap=tk.WORD)
loadlock_textbox.grid(row=1, column=1, padx=10, pady=10)

mainchamber_label = tk.Label(monitor_frame, text="Mainchamber")
mainchamber_label.grid(row=0, column=2, padx=5, pady=5)
mainchamber_textbox = tk.Text(monitor_frame, width=30, height=1, wrap=tk.WORD)
mainchamber_textbox.grid(row=1, column=2, padx=10, pady=10)

# GPT: explanation - Store the latest serial port values in variables
buffervolume.pressurevalue = tk.StringVar()
loadlock.pressurevalue = tk.StringVar()
mainchamber.pressurevalue = tk.StringVar()

# GPT: explanation - Function to update textboxes with the latest value
def update_monitor_textbox(textbox, serial_conn, latest_value):
    while True:
        if serial_conn.in_waiting > 0:
            data = serial_conn.readline().decode('utf-8').strip()
            latest_value.set(data)
            textbox.delete("1.0", tk.END)
            textbox.insert(tk.END, data)

def parse_serial_data(data_string):
    elements = data_string.split(',')
    elements = [element.strip() for element in elements]
    print(elements)
    pressure_value =float(elements[1]) #enter whatever you wanna return. We only want pressure values here
    return pressure_value

            

# GPT: explanation - Create serial connections and start threads to read serial data
serial_connections = []
# threads = []

ser1 = buffervolume.create_serial_connection()
if ser1:
    serial_connections.append(ser1)
    thread1 = threading.Thread(target=update_monitor_textbox, 
                               args=(buffervolume_textbox, ser1, buffervolume.pressurevalue), daemon=True)
    # threads.append(thread1)
    thread1.start()

ser2 = loadlock.create_serial_connection()
if ser2:
    serial_connections.append(ser2)
    thread2 = threading.Thread(target=update_monitor_textbox,
                                args=(loadlock_textbox, ser2, loadlock.pressurevalue), daemon=True)
    # threads.append(thread2)
    thread2.start()

ser3 = mainchamber.create_serial_connection()
if ser3:
    serial_connections.append(ser3)
    thread3 = threading.Thread(target=update_monitor_textbox, 
                               args=(mainchamber_textbox, ser3, mainchamber.pressurevalue), daemon=True)
    # threads.append(thread3)
    thread3.start()


# 4th row - Macros


def print_values():
    data= buffervolume.pressurevalue.get()
    print(data)
    data_parsed=parse_serial_data(data)
    print("parse:",data_parsed)
    


def call_macros_script():
    os.system('python macro_console.py')


macro_bar = ttk.LabelFrame(root, text="Macro scripts")
macro_bar.grid(row=4, column=0, padx=10, pady=10, columnspan=4, sticky="ew")

button_macros = tk.Button(macro_bar, text="macro scripts",
                          command=call_macros_script, width=30, height=5)
button_macros.grid(row=2, column=0, padx=10, pady=10)

button_values = tk.Button(macro_bar, text="Immeditate values",
                          command=print_values, width=30, height=5)
button_values.grid(row=2, column=1, padx=10, pady=10)



terminal_output = tk.Text(monitor_frame, height=10, width=80)
terminal_output.grid(row=3, column=0,columnspan=3, padx=10, pady=10)

# Redirect stdout to the terminal_output Text widget
sys.stdout = RedirectText(terminal_output)



# Start the Tkinter main loop
root.mainloop()

# Close the serial ports when the program is closed
for ser in serial_connections:
    ser.close()


