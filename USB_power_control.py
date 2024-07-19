import subprocess

def control_com_port(devcon_path, port_name, action):
    """
    Controls the power of a COM port using DevCon.

    Parameters:
    devcon_path (str): Path to devcon.exe
    port_name (str): Name of the COM port (e.g., COM6)
    action (str): 'enable' or 'disable'
    """
    if action not in ["enable", "disable"]:
        print("Invalid action. Use 'enable' or 'disable'.")
        return None

    # Find the device instance path for the given COM port
    ps_command = f"Get-WmiObject Win32_SerialPort | Where-Object {{ $_.DeviceID -eq '{port_name}' }} | Select-Object -ExpandProperty PNPDeviceID"
    command = ["powershell", "-Command", ps_command]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None

    device_id = result.stdout.strip()

    if not device_id:
        print(f"Device on {port_name} not found.")
        return None

    # Use DevCon to enable or disable the COM port
    devcon_command = [devcon_path, action, f"@{device_id}"]
    result = subprocess.run(devcon_command, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Successfully {action}d {port_name}.")
    else:
        print(f"Error: {result.stderr}")

# Example usage:
devcon_path = "C:\\DevCon\\devcon.exe"
com_port = "COM6"

# Disable the COM port
control_com_port(devcon_path, com_port, "disable")

# Wait for user input before enabling the port again
input("Press Enter to re-enable the COM port...")

# Enable the COM port
control_com_port(devcon_path, com_port, "enable")
