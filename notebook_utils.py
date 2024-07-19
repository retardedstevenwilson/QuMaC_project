import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
import serial
import threading
import time


def read_from_serial(ser):
    
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        return data
    else:
        print("NO INPUT")
    time.sleep(1)  # Add a delay to avoid constant updating




# Function to create a serial connection
def create_serial_connection(port, baud_rate):
    try:
        return serial.Serial(port, baud_rate, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        return None

# TOGGLE SWITCHES --------------------------------------------------------


def toggle_relay(relay_no,state):
    global arduino
    if state == True:
        arduino.write(f'1:{relay_no}:0\n'.encode('utf-8'))  # Send '0' to turn relay off
        print("Relay {}: ON".format(relay_no))
        time.sleep(0.1) 
    elif state ==False:
        arduino.write(f'1:{relay_no}:1\n'.encode('utf-8'))  # Send '1' to turn relay on
        print("Relay {}: OFF".format(relay_no))
        time.sleep(0.1) 
    else:
        print("Invalid command: Enter the state")
    
def timetoggle_relay(relay_no,duration):
    # Function code = 2
    global arduino
    global relay_states
    state = relay_states[relay_no]
   
    arduino.write(f'2:{relay_no}:{duration}\n'.encode('utf-8'))  # Send '0' to turn relay off
    time.sleep(duration/1000)
    
         
   

