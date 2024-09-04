import tkinter as tk
import time
import os
import serial
import time
import atexit

# Arduino class --------------------------------------------------------

class ArduinoConnector_console:
    def __init__(self, port):
        self.port = port
        self.arduino = None
        self.reset()
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
        #function code = 1
        try:
            if self.arduino and self.arduino.is_open:
                if state:
                    self.arduino.write(f'1:{relay_no}:0\n'.encode('utf-8'))  # Send '0' to turn relay on
                    line = self.arduino.readline().decode('utf-8').strip()
                    if line:
                        print(f"UNO: {line}")
                    print(f"Relay {relay_no}: ON")
                    time.sleep(0.1)
                elif state == False:
                    self.arduino.write(f'1:{relay_no}:1\n'.encode('utf-8'))  # Send '1' to turn relay off
                    line = self.arduino.readline().decode('utf-8').strip()
                    if line:
                        print(f"UNO: {line}")
                    print(f"Relay {relay_no}: OFF")
                    time.sleep(0.1)    
        except Exception as e:
            print(e)
   
    def timetoggle_relay(self,relay_no,toggletime=0.1):
        #all values are sent to arduino by converting into milliseconds
        # Function code = 2
        try:
            if self.arduino and self.arduino.is_open:
                self.arduino.write(f'2:{relay_no}:{toggletime}\n'.encode('utf-8'))  # Send '0' to turn relay off
                line = self.arduino.readline().decode('utf-8').strip()
                if line:
                    print(f"UNO: {line}")
                print(f"Relay {relay_no} toggled for {toggletime} seconds")
                time.sleep((toggletime) + 2)
        except Exception as e:
            print(e)
         
   
class pgauge_console:
    def __init__(self,name,port):
        self.port = port
        self.baudrate =9600
        self.pressurevalue = 1000
        self.name = name
        self.log_file = f"{self.name}_log.txt"
        print(f"Connection: {self.name} on {self.port}")
        # self.create_serial_connection() #making serial connection  by itself
        # self.log_serial_data() #taking values in log as soon as it starts


    # Function to create a serial connection 14 Aug (for console_2)
    def create_serial_connection(self):
        try:
           return serial.Serial(self.port, self.baudrate, timeout=1)
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port}: {e}")
            return None

    def parse_serial_data(self,data_string):
        elements = data_string.split(',')
        elements = [element.strip() for element in elements]
        print(elements)
        pressure_value =float(elements[1]) #enter whatever you wanna return. We only want pressure values here
        return pressure_value

    def read_last_entry(self):
        '''Read last entry. Return pressure value'''
        with open(self.log_file, 'rb') as file:
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
        pressure_value=self.parse_serial_data(last_entry)   
        return pressure_value


    def update_monitor_textbox(self,textbox, latest_value):
        ser = serial.Serial(self.port, self.baudrate, timeout=1)
        while True:
            if ser.in_waiting > 0:
                # Read a line from the serial port
                line = ser.readline().decode('utf-8').strip()                

                latest_value.set(line)
                textbox.delete("1.0", tk.END)
                textbox.insert(tk.END, line)

            
arduino=ArduinoConnector_console('COM6')

roughing_relay=1
buffer_to_loadlock_relay=2
N2_relay=3
O2_relay=4
loadlock_to_main_relay=5

buffervolume=pgauge_console(name='buffervolume',port='COM3') #change comport to 5 for madhavi's laptop
mainchamber=pgauge_console(name='mainchamber',port='COM7')
loadlock=pgauge_console(name='loadlock',port='COM4')


def loadlock_to_main_valve(value):
    arduino.toggle_relay(loadlock_to_main_relay,state=value)

def roughing_valve(value):
    arduino.toggle_relay(roughing_relay,state=value)


def timetoggle_buffer_to_loadlock_valve(toggletime):
    arduino.timetoggle_relay(buffer_to_loadlock_relay,toggletime=toggletime)



            
def N2_toggle(p_opt,duration=3,toggletime=0.2,initial_toggle=1.5):
    '''N2 Charging in the loadlock'''
    print("Starting N2 toggle")
    arduino.timetoggle_relay(N2_relay,toggletime=initial_toggle)
    loadlock.log_serial_data(timeout=5)
    p_current= loadlock.read_last_entry()
    
    thr=0.1*p_opt
    count=0

    try:
        while p_opt-p_current>=thr:
            arduino.timetoggle_relay(N2_relay,toggletime)
            # time.sleep(1)
            loadlock.log_serial_data(timeout=duration)
            p_current= loadlock.read_last_entry()
            print("current p = ",p_current)
            count+=1
            print("Toggle {} completed.".format(count))
            # time.sleep(5)
            print("Final mainchamber presure = {}. Toggling stopped after {} counts".format(p_current,count))
    except KeyboardInterrupt:
        print("Toggle process manually stopped")


def roughing_toggle(p_opt,duration=5):
    '''Starts roughing process in the loadlock'''
    thr=0.1*p_opt
    print("Starting roughing toggle. Opening the valve")
    roughing_valve(True)

    try:
        loadlock.log_serial_data(timeout=5)
        p_current= loadlock.read_last_entry()
        
        arduino.toggle_relay(roughing_relay,True)
        
        while p_current - p_opt >= thr:
            loadlock.log_serial_data(timeout=duration)            
            p_current= loadlock.read_last_entry()
            print("current p = {}. Roughing continues... ".format(p_current))
            time.sleep(1)
        
        print("Optimum P reached. Turning off the roughing relay")
        arduino.toggle_relay(roughing_relay,False)
    
    except KeyboardInterrupt:
        print("Roughing toggle manually stopped")
        arduino.toggle_relay(roughing_relay,False)
        
    print("Final mainchamber presure = {}".format(p_current))

    


    
    