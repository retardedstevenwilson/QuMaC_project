import tkinter as tk
import serial
import time

# Configure the serial port to which the Arduino is connected
arduino = serial.Serial('COM6', 9600)  # Change 'COM6' to your Arduino port
time.sleep(2)  # Give some time for the connection to be established

relay_states = {2: False, 3: False, 4: False,5: False}


def toggle_relay(button, relay_no):
    global relay_states
    global arduino
    state = relay_states[relay_no]
    if state:
        arduino.write(f'{relay_no}.0\n'.encode('utf-8'))  # Send '0' to turn relay off
        button.config(text="Relay {relay_no}: ON", bg='green', fg='white')
    else:
        arduino.write(f'{relay_no}.1\n'.encode('utf-8'))  # Send '1' to turn relay on
        button.config(text="Relay {relay_no}: OFF", bg='red', fg='white')
    relay_states[relay_no] = not state

# Create the main window
root = tk.Tk()
root.title("Arduino Relay Control")

# Create buttons to toggle the relays
button_1 = tk.Button(root, text="OFF", command=lambda: toggle_relay(button_1, 2), width=15, height=5)
button_1.pack(pady=20)

button_2 = tk.Button(root, text="OFF", command=lambda: toggle_relay(button_2, 3), width=15, height=5)
button_2.pack(pady=20)

button_3 = tk.Button(root, text="OFF", command=lambda: toggle_relay(button_3, 4), width=15, height=5)
button_3.pack(pady=20)

button_4 = tk.Button(root, text="OFF", command=lambda: toggle_relay(button_4, 5), width=15, height=5)
button_4.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
