import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
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
    

def toggle():
    toggle_btn = tk.Button(text="Toggle", width=12, relief="raised")
    toggle_btn.grid(row = 1, column = 0, pady = 2)
    if toggle_btn.config('relief')[-1] == 'sunken':
        toggle_btn.config(relief="raised")
    else:
        toggle_btn.config(relief="sunken")



# Define our switch function
def button_mode():
   global is_on
   # Determine it is on or off
   if is_on:
      on_.config(image=off)
    #   label.config(text="Day Mode is On", bg="white", fg="black")
      is_on = False
   else:
      on_.config(image=on)
    #   label.config(text="Night Mode is On", fg="black")
      is_on = True





# Create the main window
root = tk.Tk()
root.title("Serial Monitors")
# root.geometry("500x300")


# Keep track of the button state on/off
#global is_on
is_on = True


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
    label.grid(row = 1, column = i, pady = 2)
    frames[i].grid(row = 0, column = i, pady = 2)
    textbox = scrolledtext.ScrolledText(frames[i], width=40, height=5, wrap=tk.WORD)
    textbox.grid(row = 0, column = i, pady = 2)
    textboxes.append(textbox)

    ser = create_serial_connection(serial_ports[i], baud_rate)
    if ser:
        serial_connections.append(ser)
        thread = threading.Thread(target=read_from_serial, args=(ser, textbox), daemon=True)
        threads.append(thread)
        thread.start()

 
toggle_btn = tk.Button(text="Toggle", width=12, relief="raised", command=toggle)

# Define Our Images
on = PhotoImage(file="E:\QuMaC\Codes\on.jpg")
off = PhotoImage(file="E:\QuMaC\Codes\off.jpg")
# Create A Button

on_ = tk.Button(root, image=on, bd=0, command=button_mode,text='Relay1', height=100, width=100)
on_.grid(row = 2, column = 0, pady = 2)
# on_2 = tk.Button(root, image=on, bd=0, command=button_mode,text='Relay1', height=100, width=100)
# on_2.grid(row = 2, column = 1, pady = 2)
# on_3 = tk.Button(root, image=on, bd=0, command=button_mode,text='Relay1', height=100, width=100)
# on_3.grid(row = 2, column = 2, pady = 2)
# on_4 = tk.Button(root, image=on, bd=0, command=button_mode,text='Relay1', height=100, width=100)
# on_4.grid(row = 2, column = 3, pady = 2)






# Start the Tkinter main loop
root.mainloop()

# Close the serial ports when the program is closed
for ser in serial_connections:
    ser.close()