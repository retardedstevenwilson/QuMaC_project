import tkinter as tk
from tkinter import scrolledtext
import serial
import threading
import time

#trying the git push 

# Function to read from a serial port
def read_from_serial(ser, textbox):
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            update_textbox(textbox, data)
        else:
            update_textbox(textbox, "NO INPUT")
        time.sleep(1)  # Add a delay to avoid constant updating

# Function to update the text box in the GUI
def update_textbox(textbox, data):
    textbox.insert(tk.END, data + "\n")
    textbox.see(tk.END)  # Scroll to the end

# Function to create a serial connection
def create_serial_connection(port, baud_rate):
    try:
        return serial.Serial(port, baud_rate, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        return None

# Create the main window
root = tk.Tk()
root.title("Serial Monitors")

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
    frames[i].pack(side=tk.LEFT, padx=10, pady=10)
    label = tk.Label(frames[i], text=titles[i])
    label.pack()
    textbox = scrolledtext.ScrolledText(frames[i], width=40, height=10, wrap=tk.WORD)
    textbox.pack()
    textboxes.append(textbox)

    ser = create_serial_connection(serial_ports[i], baud_rate)
    if ser:
        serial_connections.append(ser)
        thread = threading.Thread(target=read_from_serial, args=(ser, textbox), daemon=True)
        threads.append(thread)
        thread.start()

# Start the Tkinter main loop
root.mainloop()

# Close the serial ports when the program is closed
for ser in serial_connections:
    ser.close()