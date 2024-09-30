import tkinter as tk
from tkinter import ttk
import threading
import time
import sys
import os
import serial
import atexit

# from console_2_toolkit import *
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
        self.pressurevalue = -1
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



# class RedirectText:
#     def __init__(self, text_widget):
#         self.text_widget = text_widget

#     def write(self, string):
#         self.text_widget.insert(tk.END, string)
#         self.text_widget.see(tk.END)

#     def flush(self):
#         pass  # Required for file-like object interface
    


#------------------------------------------HARDCONNECTIONS---------------------------------------------------

arduino=ArduinoConnector_console('COM6')

roughing_relay=1
buffer_to_loadlock_relay=2
N2_relay=3
O2_relay=4
loadlock_to_main_relay=5

buffervolume=pgauge_console(name='buffervolume',port='COM3') #change comport to 5 for madhavi's laptop
mainchamber=pgauge_console(name='mainchamber',port='COM7')
loadlock=pgauge_console(name='loadlock',port='COM4')


# Create the main window
root = tk.Tk()
root.title("Master Console")
root.configure(background='brown')
root.geometry("900x500")

# First row - Monitors
monitor_frame = ttk.LabelFrame(root, text="Monitors", border=10)
monitor_frame.grid(row=0, column=0, padx=5, pady=5, columnspan=1, sticky="ew")
baud_rate = 9600

# Create individual labels and textboxes for monitors
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

# Store the latest serial port values in variables
buffervolume.pressurevalue = tk.StringVar()
loadlock.pressurevalue = tk.StringVar()
mainchamber.pressurevalue = tk.StringVar()

# DISPLAY
terminal_output = tk.Text(monitor_frame, height=10, width=80)
terminal_output.grid(row=3, column=0,columnspan=3, padx=10, pady=10)




# GPT: explanation - Function to update textboxes with the latest value
def update_monitor_textbox(textbox, serial_conn, latest_value):
    while True:
        if serial_conn.in_waiting > 0:
            data = serial_conn.readline().decode('utf-8').strip()
            latest_value.set(data)
            textbox.delete("1.0", tk.END)
            pvalues=parse_serial_data(data)
            textbox.insert(tk.END, pvalues)

def parse_serial_data(data_string):
    elements = data_string.split(',')
    elements = [element.strip() for element in elements]
    pressure_value =float(elements[1]) #enter whatever you wanna return. We only want pressure values here
    return pressure_value

            

#  Create serial connections and start threads to read serial data
serial_connections = []

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
    

def create_popup(title, func, defaults):
    popup = tk.Toplevel()
    popup.title(title)

    arg_entries = {}
    for arg, default in defaults.items():
        frame = ttk.Frame(popup)
        frame.pack(fill='x', padx=5, pady=5)

        label = ttk.Label(frame, text=f"{arg}:")
        label.pack(side='left', padx=5, pady=5)

        entry = ttk.Entry(frame)
        entry.insert(0, default)
        entry.pack(fill='x', expand=True)
        arg_entries[arg] = entry

    def execute():
        args = {arg: entry.get() for arg, entry in arg_entries.items()}
        popup.destroy()
        func(**args)

    button_frame = ttk.Frame(popup)
    button_frame.pack(fill='x', padx=5, pady=5)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=popup.destroy)
    cancel_button.pack(side='right', padx=5, pady=5)

    execute_button = ttk.Button(button_frame, text="Execute", command=execute)
    execute_button.pack(side='right', padx=5, pady=5)


######################################### MACRO FUNCTIONS ###################################################

#O2 charging functions
def funct1_O2_buffer_toggle(p_opt,duration=10,toggletime=0.1):
    p_opt=float(p_opt)
    duration=float(duration)
    toggletime=float(toggletime)

    print("Starting O2 toggle")
    '''inputs: p_opt, duration of logging after each toggle, and toggletime'''
    p_current= buffervolume.pressurevalue.get()
    p_current=parse_serial_data(p_current)

    print("p_o2_current = ",p_current)
    thr=0.1
    p_max=760
    if p_current >=p_max:
        print('ALERT: BUFFER PRESSURE REACHED MAXIMUM')
    else:
        count=0    
        while p_opt-p_current>=thr:
            arduino.timetoggle_relay(O2_relay,toggletime)
            print("P_current_bv = ",p_current)
            print("Toggling. Standby for 5 sec")
            time.sleep(5)
            p_current= buffervolume.pressurevalue.get()
            p_current=parse_serial_data(p_current)
            count+=1
            print("Toggle {} completed.".format(count))
            # time.sleep(5)
    print("Final buffer presure = {}. Toggling stopped after {} counts".format(p_current,count))

def funct2_function_b(arg1, arg2):
    print(f"Function B called with arg1={arg1}, arg2={arg2}")

def funct3_print_values():
    data= buffervolume.pressurevalue.get()
    print(data)
    data_parsed=parse_serial_data(data)
    print("parse:",data_parsed)


########################### Making popup for buttons and assigning macro functions to them ################################
def button1_o2charge():
    create_popup('O2 Charge', funct1_O2_buffer_toggle, 
                            {'p_opt': 40, 'duration': 10, 'toggletime': 0.1}) # funct1_O2_buffer_toggle(p_opt,duration=10,toggletime=0.1):


def button2_function_b():
    create_popup('Function B', funct2_function_b,
                        {'arg1': 'enter', 'arg2': 'something'})


macro_bar = ttk.LabelFrame(root, text="Macro scripts")
macro_bar.grid(row=4, column=0, padx=10, pady=10, columnspan=4, sticky="ew")



button_values = tk.Button(macro_bar, text="Immediate values",
                          command=funct3_print_values, width=30, height=5)
button_values.grid(row=2, column=1, padx=10, pady=10)

o2_charge = tk.Button(macro_bar, text="O2 charge",
                          command=button1_o2charge, width=30, height=5)
o2_charge.grid(row=2, column=2, padx=10, pady=10)

functb_button = tk.Button(macro_bar, text="functb",
                          command=button2_function_b, width=30, height=5)
functb_button.grid(row=2, column=3, padx=10, pady=10)



# Second row - Pump Toggles-------------------------------------------------------------------------------
pump_toggle_frame = ttk.LabelFrame(root, text="Toggles")
pump_toggle_frame.grid(row=5, column=0, padx=10, pady=10, columnspan=4, sticky="ew")


# # Create buttons to toggle the relays
# button_1 = tk.Button(pump_toggle_frame, text="Relay 1: OFF", command=lambda: arduino.toggle_relay(button_1, 1), width=15, height=5)
# button_1.grid(row = 2, column = 0,  padx=10, pady=10)

# button_2 = tk.Button(pump_toggle_frame, text="Relay 2: OFF", command=lambda: arduino.toggle_relay(button_2, 2), width=15, height=5)
# button_2.grid(row = 2, column = 1,  padx=10, pady=10)

# button_3 = tk.Button(pump_toggle_frame, text="Relay 3: OFF", command=lambda: arduino.toggle_relay(button_3, 3), width=15, height=5)
# button_3.grid(row = 2, column = 2,  padx=10, pady=10)

# button_4 = tk.Button(pump_toggle_frame, text="Relay 4: OFF", command=lambda: arduino.toggle_relay(button_4, 4), width=15, height=5)
# button_4.grid(row = 2, column = 3,  padx=10, pady=10)





# # DISPLAY
# terminal_output = tk.Text(monitor_frame, height=10, width=80)
# terminal_output.grid(row=3, column=0,columnspan=3, padx=10, pady=10)
# # Redirect stdout to the terminal_output Text widget
# # sys.stdout = RedirectText(terminal_output)



def quit(event):
    root.quit()

root.bind('<Control-c>', quit)
root.mainloop()


# Close the serial ports when the program is closed
for ser in serial_connections:
    ser.close()


