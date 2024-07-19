import tkinter as tk
from tkinter import ttk

# Initialize the main window
root = tk.Tk()
root.title("Tkinter GUI Example")
root.geometry("1024x468")

# First row - Monitors
monitor_frame = ttk.LabelFrame(root, text="Monitors")
monitor_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=4, sticky="ew")

titles = ["Monitor 1", "Monitor 2", "Monitor 3", "Terminal Output"]
for i in range(3):
    label = tk.Label(monitor_frame, text=titles[i])
    label.grid(row=0, column=i, padx=10, pady=10)

terminal_output = tk.Text(monitor_frame, height=5, width=20)
terminal_output.grid(row=0, column=3, padx=10, pady=10)

# Second row - Pump Toggles
pump_toggle_frame = ttk.LabelFrame(root, text="Pump Toggles")
pump_toggle_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=4, sticky="ew")

for i in range(2):
    for j in range(6):
        button = tk.Button(pump_toggle_frame, text=f"Relay {i*6+j+1}: OFF", width=15, height=5)
        button.grid(row=i, column=j, padx=10, pady=10)

# Third row - Time Toggles
time_toggle_frame = ttk.LabelFrame(root, text="Time Toggles")
time_toggle_frame.grid(row=2, column=0, padx=10, pady=10, columnspan=4, sticky="ew")


# Run the application
root.mainloop()

