import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
import serial
import threading
import time


# MONITOR READING --------------------------------------------------------
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

# TOGGLE SWITCHES --------------------------------------------------------


def toggle_relay(button, relay_no):
    global arduino
    global relay_states
    state = relay_states[relay_no]
    if state:
        arduino.write(f'1:{relay_no}:0\n'.encode('utf-8'))  # Send '0' to turn relay off
        button.config(text=f"Relay {relay_no}: ON", bg='green', fg='white',width=15, height=5)
        print("Relay {}: ON".format(relay_no))
        time.sleep(0.1) 
    else:
        arduino.write(f'1:{relay_no}:1\n'.encode('utf-8'))  # Send '1' to turn relay on
        button.config(text=f"Relay {relay_no}: OFF", bg='red', fg='white',width=15, height=5)
        print("Relay {}: OFF".format(relay_no))
        time.sleep(0.1) 
    relay_states[relay_no] = not state
    
def timetoggle_relay(button, relay_no,duration):
    # Function code = 2
    global arduino
    global relay_states
    state = relay_states[relay_no]
    if state:
        arduino.write(f'2:{relay_no}:{duration}\n'.encode('utf-8'))  # Send '0' to turn relay off
        button.config(text=f"Relay {relay_no}: ON", bg='green', fg='white',width=15, height=5)
        time.sleep(0.1)
        button.config(text=f"Relay {relay_no}: OFF", bg='red', fg='white',width=15, height=5)
         
    else:
        print("Relay {} is already ON".format(relay_no))
        time.sleep(0.1) 


