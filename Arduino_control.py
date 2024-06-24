import serial.tools.list_ports

ports=serial.tools.list_ports.comports()

SerialInst= serial.Serial()

portslist=[]

for element in ports:
    portslist.append(str(element))
    print(element)


com = input("Select COM port for the Arduino: ")

for i in range(len(portslist)):
    if portslist[i].startswith("COM" +str(com)):
        use = "COM" + str(com)
        print(use)
        

SerialInst.baudrate = 9600
SerialInst.port = use
SerialInst.open()

while True:
    command= input("Command: ")
    SerialInst.write(command.encode('utf-8'))

    if command == 'exit':
        quit()