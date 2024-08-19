import automation_utils_master_console as Q
import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
from tkinter import ttk
import serial
import threading
import time
import sys
import os

# Q.arduino = serial.Serial('COM6', 9600)  # Change 'COM6' to your Arduino port
time.sleep(2)  # Give some time for the connection to be established

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


def call_macros_script():
    os.system('python macro_console.py')


# Create the main window
root = tk.Tk()
root.title("Master Console")
root.configure(background='brown')
root.geometry("1960x800")


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



titles = ["Monitor 1", "Monitor 2", "Monitor 3", "Terminal Output"]
for i in range(3):
    label = tk.Label(monitor_frame, text=titles[i])
    label.grid(row=0, column=i, padx=5, pady=5)
    monitor_frame.grid(row = 0, column = i,  padx=10, pady=10)
    textbox = scrolledtext.ScrolledText(monitor_frame, width=30, height=5, wrap=tk.WORD)
    textbox.grid(row = 0, column = i,  padx=10, pady=10)
    textboxes.append(textbox)

    ser = Q.create_serial_connection(serial_ports[i], baud_rate)
    if ser:
        serial_connections.append(ser)
        thread = threading.Thread(target=Q.read_from_serial, args=(ser, textbox), daemon=True)
        threads.append(thread)
        thread.start()  #might create a memory problem

terminal_output = tk.Text(monitor_frame, height=10, width=40)
terminal_output.grid(row=0, column=3, padx=10, pady=10)

# Redirect stdout to the terminal_output Text widget
sys.stdout = RedirectText(terminal_output)



# Second row - Pump Toggles-------------------------------------------------------------------------------
pump_toggle_frame = ttk.LabelFrame(root, text="Pump Toggles")
pump_toggle_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=4, sticky="ew")

# Create buttons to toggle the relays
button_1 = tk.Button(pump_toggle_frame, text="Relay 1: OFF", command=lambda: Q.toggle_relay(button_1, 1), width=15, height=5)
button_1.grid(row = 2, column = 0,  padx=10, pady=10)

button_2 = tk.Button(pump_toggle_frame, text="Relay 2: OFF", command=lambda: Q.toggle_relay(button_2, 2), width=15, height=5)
button_2.grid(row = 2, column = 1,  padx=10, pady=10)

button_3 = tk.Button(pump_toggle_frame, text="Relay 3: OFF", command=lambda: Q.toggle_relay(button_3, 3), width=15, height=5)
button_3.grid(row = 2, column = 2,  padx=10, pady=10)

button_4 = tk.Button(pump_toggle_frame, text="Relay 4: OFF", command=lambda: Q.toggle_relay(button_4, 4), width=15, height=5)
button_4.grid(row = 2, column = 3,  padx=10, pady=10)

button_5 = tk.Button(pump_toggle_frame, text="Relay 5: OFF", command=lambda: Q.toggle_relay(button_5, 5), width=15, height=5)
button_5.grid(row = 2, column = 4,  padx=10, pady=10)

button_6 = tk.Button(pump_toggle_frame, text="Relay 6: OFF", command=lambda: Q.toggle_relay(button_6, 6), width=15, height=5)
button_6.grid(row = 2, column = 5,  padx=10, pady=10)

button_7 = tk.Button(pump_toggle_frame, text="Relay 7: OFF", command=lambda: Q.toggle_relay(button_7, 7), width=15, height=5)
button_7.grid(row = 2, column = 6,  padx=10, pady=10)

button_8 = tk.Button(pump_toggle_frame, text="Relay 8: OFF", command=lambda: Q.toggle_relay(button_8, 8), width=15, height=5)
button_8.grid(row = 2, column = 7,  padx=10, pady=10)



# Third row - Pump  timing Toggles
time_toggle_frame = ttk.LabelFrame(root, text="Time Toggles")
time_toggle_frame.grid(row=2, column=0, padx=10, pady=10, columnspan=4, sticky="ew")

inputtxt_1_timers = tk.Text(time_toggle_frame,height = 1,width = 10) 
inputtxt_1_timers.grid (row = 3, column = 0,  padx=10, pady=10)

button = tk.Button(text="Save (ms)", command= lambda: save_textbox_input(inputtxt_1_timers))
button.grid(row = 3, column = 1,  padx=10, pady=10)

# textbox_time = tk.Text(time_toggle_frame,height = 1,width = 10)
# textbox.grid(row =3, column = 2,  padx=10, pady=10)



button_1_timers = tk.Button(time_toggle_frame, text="Relay 1", width=15, height=5,
                            command=lambda: Q.timetoggle_relay(button_1, 1,toggletime))
button_1_timers.grid(row = 2, column = 0,  padx=10, pady=10)

button_2_timers = tk.Button(time_toggle_frame, text="Relay 2", 
                            command=lambda: Q.timetoggle_relay(button_2, 2,toggletime), width=15, height=5)
button_2_timers.grid(row = 2, column = 1,  padx=10, pady=10)

button_3_timers = tk.Button(time_toggle_frame, text="Relay 3",
                            command=lambda: Q.timetoggle_relay(button_3, 3,toggletime), width=15, height=5)
button_3_timers.grid(row = 2, column = 2,  padx=10, pady=10)

button_4_timers = tk.Button(time_toggle_frame, text="Relay 4",
                            command=lambda: Q.timetoggle_relay(button_4, 4,toggletime), width=15, height=5)
button_4_timers.grid(row = 2, column = 3,  padx=10, pady=10)

button_5_timers = tk.Button(time_toggle_frame, text="Relay 5",
                           command=lambda: Q.timetoggle_relay(button_5, 5,toggletime), width=15, height=5)
button_5_timers.grid(row = 2, column = 4,  padx=10, pady=10)

button_6_timers = tk.Button(time_toggle_frame, text="Relay 6",
                            command=lambda: Q.timetoggle_relay(button_6, 6,toggletime), width=15, height=5)
button_6_timers.grid(row = 2, column = 5,  padx=10, pady=10)

button_7_timers = tk.Button(time_toggle_frame, text="Relay 7",
                            command=lambda: Q.timetoggle_relay(button_7, 7,toggletime), width=15, height=5)
button_7_timers.grid(row = 2, column = 6,  padx=10, pady=10)

button_8_timers = tk.Button(time_toggle_frame, text="Relay 8",
                            command=lambda: Q.timetoggle_relay(button_8, 8,toggletime), width=15, height=5)
button_8_timers.grid(row = 2, column = 7,  padx=10, pady=10)



# 4th row - Macros
macro_bar = ttk.LabelFrame(root, text="Macro scripts")
macro_bar.grid(row=4, column=0, padx=10, pady=10, columnspan=4, sticky="ew")


button_macros = tk.Button(macro_bar, text="macro scripts",
                            command= call_macros_script, width=15, height=5)
button_macros.grid(row = 2, column =0,  padx=10, pady=10)






# Start the Tkinter main loop
root.mainloop()

    

# Close the serial ports when the program is closed
for ser in serial_connections:
    ser.close()


#turning off all relays when exiting ?????
for relay_no in range(1,4,1):
    toggle_off(relay_no)
