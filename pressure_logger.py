import serial
import time

def log_serial_data(port, baud_rate, log_file):
    # Open the serial port
    ser = serial.Serial(port, baud_rate, timeout=1)
    
    # Open the log file in append mode
    with open(log_file, 'a') as file:
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
        finally:
            # Close the serial port
            ser.close()

# Set the parameters
port = 'COM4'
baud_rate = 9600  # Adjust based on your device's settings
log_file = 'pressure_log.txt'

# Start logging
log_serial_data(port, baud_rate, log_file)
