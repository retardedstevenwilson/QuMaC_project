import serial

# Open the serial port (COM4) with appropriate settings
ser = serial.Serial('COM4', baudrate=9600, timeout=1)

try:
    while True:
        # Read a line from the serial port
        line = ser.readline().decode('utf-8').strip()
        if line:
            print(f"Received: {line}")
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    # Close the serial port
    ser.close()
