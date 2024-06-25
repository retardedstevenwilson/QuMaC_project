import tkinter as tk
import serial
import time

# Configure the serial port to which the Arduino is connected
arduino = serial.Serial('COM6', 9600)  # Change 'COM3' to your Arduino port
time.sleep(2)  # Give some time for the connection to be established


def toggle_relay():
    global relay_state
    if relay_state:
        arduino.write(b'0')  # Send '0' to turn relay off
        button.config(text="ON",bg='green', fg='white')
    else:
        arduino.write(b'1')  # Send '1' to turn relay on
        button.config(text="OFF",bg='red', fg='white')
    relay_state = not relay_state

# Create the main window
root = tk.Tk()
root.title("Arduino Relay Control")

# Initial state of the relay
relay_state = False

# Create a button to toggle the relay
button = tk.Button(root, text="Turn Relay On", command=toggle_relay, width=25, height=5)
button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
