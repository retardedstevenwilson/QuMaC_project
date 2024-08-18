
import tkinter as tk
from tkinter import ttk
# from tkinter import simpledialog4
from hardconnections import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Macros")

        # Dropdown menu setup
        self.selected_option = tk.StringVar()
        self.dropdown = ttk.Combobox(self, textvariable=self.selected_option)
        self.dropdown['values'] = ('O2 Charge', 'Function B', 'Function C')
        self.dropdown.current(0)
        self.dropdown.pack(pady=10)

        # Button to trigger pop-up
        self.button = ttk.Button(self, text="Open Pop-up", command=self.open_popup)
        self.button.pack(pady=10)

    def open_popup(self):
        selected_function = self.selected_option.get()

        # Open a new pop-up window based on the selected function
        if selected_function == 'O2 Charge':
            self.create_popup('O2 Charge', O2_buffer_toggle, 
                              {'p_opt': 40, 'duration': 10, 'toggletime': 0.1}) # O2_buffer_toggle(p_opt,duration=10,toggletime=0.1):
        
        elif selected_function == 'Function B':
            self.create_popup('Function B', self.function_b,
                               {'arg1': 'hello', 'arg2': 'world'})
        
        elif selected_function == 'Function C':
            self.create_popup('Function C', self.function_c, 
                              {'arg1': 3.14, 'arg2': 2.72})

    def create_popup(self, title, func, defaults):
        popup = tk.Toplevel(self)
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
            func(**args)
            popup.destroy()

        button_frame = ttk.Frame(popup)
        button_frame.pack(fill='x', padx=5, pady=5)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=popup.destroy)
        cancel_button.pack(side='right', padx=5, pady=5)

        execute_button = ttk.Button(button_frame, text="Execute", command=execute)
        execute_button.pack(side='right', padx=5, pady=5)


    def function_b(self, arg1, arg2):
        print(f"Function B called with arg1={arg1}, arg2={arg2}")

    def function_c(self, arg1, arg2):
        print(f"Function C called with arg1={arg1}, arg2={arg2}")



if __name__ == "__main__":
    app = App()
    app.geometry('600x150')
    app.mainloop()
