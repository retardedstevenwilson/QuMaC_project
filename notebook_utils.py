import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
import threading
import time
import os
import serial
import time
import atexit



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

# Arduino class --------------------------------------------------------


class ArduinoConnector:
    def __init__(self, port):
        self.port = port
        self.arduino = None
        self.cleanup()
        self.connect()
        atexit.register(self.reset_and_close)

    def cleanup(self):
        # Close any existing connection to free up the port
        try:
            temp_connection = serial.Serial(self.port, 9600, timeout=1)
            temp_connection.close()
            print(f"Cleaned up any previous connections on {self.port}")
        except serial.SerialException as e:
            print(e)

    def connect(self):
        try:
            self.arduino = serial.Serial(self.port, 9600, timeout=1)
            time.sleep(2)  # Wait for the connection to be established
            print(f"Connected to Arduino on {self.port}")
        except serial.SerialException as e:
            print(f"Error: {e}")

    def reset(self):
        if self.arduino and self.arduino.is_open:
            print("Resetting Arduino...")
            self.arduino.setDTR(False)
            time.sleep(1)
            self.arduino.setDTR(True)
            time.sleep(2)
            print("Arduino has been reset.")

    def reset_and_close(self):
        self.reset()
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.close()
                print("Connection to Arduino closed.")
            except Exception as e:
                print(e)
        else:
            print("arduino is not conntected")
    

    def toggle_relay(self, relay_no, state):
        try:
            if self.arduino and self.arduino.is_open:
                if state:
                    self.arduino.write(f'1:{relay_no}:0\n'.encode('utf-8'))  # Send '0' to turn relay on
                    print(f"Relay {relay_no}: ON")
                    time.sleep(0.1)
                elif state == False:
                    self.arduino.write(f'1:{relay_no}:1\n'.encode('utf-8'))  # Send '1' to turn relay off
                    print(f"Relay {relay_no}: OFF")
                    time.sleep(0.1)    
        except Exception as e:
            print(e)
   
    def timetoggle_relay(self,relay_no,duration):
        # Function code = 2
        try:
            if self.arduino and self.arduino.is_open:
                self.arduino.write(f'2:{relay_no}:{duration}\n'.encode('utf-8'))  # Send '0' to turn relay off
                print(f"Relay {relay_no} toggled for {duration} ms")
                time.sleep(duration/1000)
        except Exception as e:
            print(e)
         
   
# class pgauge:
#     def __init__(self, port):
#         self.port = port
#         self.cleanup()
#         self.connect()
#         atexit.register(self.reset_and_close)


def log_serial_data(port, baud_rate, log_file,timeout=0):
    # Open the serial port
    ser = serial.Serial(port, baud_rate, timeout=1)
    
    # Open the log file in append mode
    with open(log_file, 'a') as file:
        if timeout == 0:
            print("Logging started. Press Ctrl+C to stop.")
            try:
                while True:
                    # Read a line from the serial port
                    line = ser.readline().decode('utf-8').strip()                
                    if line:
                        # Print the line to the console
                        print(line)
                        # Write the line to the log file with a timestamp
                        file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {line}\n")        
            except KeyboardInterrupt:
                print("Logging stopped.")
        else:
            print("Logging started for {} seconds. Press Ctrl+C to stop.".format(timeout))
            t_init= time.time()
            try:
                while time.time()-t_init < timeout:
                        # Read a line from the serial port
                        line = ser.readline().decode('utf-8').strip()
                        if line:
                            # Print the line to the console
                            print(line)
                            # Write the line to the log file with a timestamp
                            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {line}\n")                        
            except Exception as e:
                print(e)
        #reading the last entry
        print("final pressure =: ",read_last_entry(log_file))
        # Close the serial port
        ser.close()



def read_last_entry(log_file):
    with open(log_file, 'rb') as file:
        # Move the cursor to the end of the file
        file.seek(0, os.SEEK_END)
        # Initialize variables to track the position and buffer
        position = file.tell()
        buffer = b''       
        # Traverse backwards in the file
        while position > 0:
            # Move cursor back by one byte
            position -= 1
            file.seek(position)
            # Read the byte at the current position
            byte = file.read(1)            
            # Prepend the byte to the buffer
            buffer = byte + buffer
            # Check for newline character (indicating the end of the last line)
            if byte == b'\n' and buffer != b'\n':
                # Break if we've reached the start of the last line
                break      
        # Decode the buffer to get the last line as a string, stripping any trailing newline characters
        last_entry = buffer.decode('utf-8').strip()
        print(last_entry)     
    return last_entry






# def pressure_toggle(port,log_file,p_opt,relay,toggletime):
#     global baud_rate
#     log_serial_data(port, baud_rate, log_file)
#     time.sleep(10)
#     KeyboardInterrupt
#     p_current=read_last_entry(log_file)
#     while p_current - p_opt < 0.1 *p_opt :
#         log_serial_data(port, baud_rate, log_file)
#         time.sleep(5)
#         KeyboardInterrupt
#         p_current=read_last_entry(log_file)

    


    
    