import Automation_utils as Q
import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
import serial
import threading
import time



Q.arduino = serial.Serial('COM6', 9600)  # Change 'COM6' to your Arduino port
time.sleep(2)  # Give some time for the connection to be established

Q.relay_states = {2: False, 3: False, 4: False,5: False}



# Create the main window
root = tk.Tk()
root.title("Master Console")


# Create a frame for each monitor
frames = [tk.Frame(root) for _ in range(3)]
titles = ["Monitor 1", "Monitor 2", "Monitor 3"]
serial_ports = ['COM3', 'COM4', 'COM5']  # Change these as necessary
baud_rate = 9600

# Create serial connections and text widgets
serial_connections = []
textboxes = []
threads = []



for i in range(3):
    label = tk.Label(frames[i], text=titles[i])
    label.grid(row = 1, column = i,  padx=10, pady=10)
    frames[i].grid(row = 0, column = i,  padx=10, pady=10)
    textbox = scrolledtext.ScrolledText(frames[i], width=40, height=5, wrap=tk.WORD)
    textbox.grid(row = 0, column = i,  padx=10, pady=10)
    
    textboxes.append(textbox)

    ser = Q.create_serial_connection(serial_ports[i], baud_rate)
    if ser:
        serial_connections.append(ser)
        thread = threading.Thread(target=Q.read_from_serial, args=(ser, textbox), daemon=True)
        threads.append(thread)
        thread.start()



# Create buttons to toggle the relays
button_1 = tk.Button(root, text="Relay 1: OFF", command=lambda: Q.toggle_relay(button_1, 2), width=15, height=5)
button_1.grid(row = 2, column = 0,  padx=10, pady=10)

button_2 = tk.Button(root, text="Relay 2: OFF", command=lambda: Q.toggle_relay(button_2, 3), width=15, height=5)
button_2.grid(row = 2, column = 1,  padx=10, pady=10)

button_3 = tk.Button(root, text="Relay 3: OFF", command=lambda: Q.toggle_relay(button_3, 4), width=15, height=5)
button_3.grid(row = 2, column = 2,  padx=10, pady=10)

button_4 = tk.Button(root, text="Relay 4: OFF", command=lambda: Q.toggle_relay(button_4, 5), width=15, height=5)
button_4.grid(row = 2, column = 3,  padx=10, pady=10)


# Start the Tkinter main loop
root.mainloop()

# Close the serial ports when the program is closed
for ser in serial_connections:
    ser.close()