import tkinter as tk
from tkinter import ttk
import threading
import time
import sys
import os
from console_2_toolkit import *



class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):
        pass  # Required for file-like object interface
    


# Create the main window
root = tk.Tk()
root.title("Master Console")
root.configure(background='brown')
root.geometry("900x500")

# First row - Monitors
monitor_frame = ttk.LabelFrame(root, text="Monitors", border=10)
monitor_frame.grid(row=0, column=0, padx=5, pady=5, columnspan=1, sticky="ew")
baud_rate = 9600

# GPT: explanation - Create individual labels and textboxes for monitors
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

# GPT: explanation - Store the latest serial port values in variables
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

            

# GPT: explanation - Create serial connections and start threads to read serial data
serial_connections = []
# threads = []

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


# 4th row - Macros
# Dropdown menu setup

def print_values():
    data= buffervolume.pressurevalue.get()
    print(data)
    data_parsed=parse_serial_data(data)
    print("parse:",data_parsed)
    

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





# def open_popup(funct):
#     selected_function = funct

#     # Open a new pop-up window based on the selected function
#     if selected_function == 'O2 Charge':
#         create_popup('O2 Charge', O2_buffer_toggle, 
#                             {'p_opt': 40, 'duration': 10, 'toggletime': 0.1}) # O2_buffer_toggle(p_opt,duration=10,toggletime=0.1):
    
#     elif selected_function == 'Function B':
#         create_popup('Function B', function_b,
#                             {'arg1': 'hello', 'arg2': 'world'})
    
#     elif selected_function == 'Function C':
#         create_popup('Function C', function_c, 
#                             {'arg1': 3.14, 'arg2': 2.72})


#O2 charging functions
def O2_buffer_toggle(p_opt,duration=10,toggletime=0.1):
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


def button_o2charge():
    create_popup('O2 Charge', O2_buffer_toggle, 
                            {'p_opt': 40, 'duration': 10, 'toggletime': 0.1}) # O2_buffer_toggle(p_opt,duration=10,toggletime=0.1):


def button_function_b():
    create_popup('Function B', function_b,
                        {'arg1': 'enter', 'arg2': 'something'})

def function_b(arg1, arg2):
    print(f"Function B called with arg1={arg1}, arg2={arg2}")



macro_bar = ttk.LabelFrame(root, text="Macro scripts")
macro_bar.grid(row=4, column=0, padx=10, pady=10, columnspan=4, sticky="ew")

# button_macros = tk.Button(macro_bar, text="macro scripts",
#                           command=call_macros_script, width=30, height=5)
# button_macros.grid(row=2, column=0, padx=10, pady=10)

button_values = tk.Button(macro_bar, text="Immediate values",
                          command=print_values, width=30, height=5)
button_values.grid(row=2, column=1, padx=10, pady=10)

o2_charge = tk.Button(macro_bar, text="O2 charge",
                          command=button_o2charge, width=30, height=5)
o2_charge.grid(row=2, column=2, padx=10, pady=10)

functb_button = tk.Button(macro_bar, text="functb",
                          command=button_function_b, width=30, height=5)
functb_button.grid(row=2, column=3, padx=10, pady=10)






# DISPLAY
terminal_output = tk.Text(monitor_frame, height=10, width=80)
terminal_output.grid(row=3, column=0,columnspan=3, padx=10, pady=10)


# Redirect stdout to the terminal_output Text widget
# sys.stdout = RedirectText(terminal_output)


def quit(event):
    root.quit()

root.bind('<Control-c>', quit)
root.mainloop()


# Close the serial ports when the program is closed
for ser in serial_connections:
    ser.close()


