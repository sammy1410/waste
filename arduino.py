import streamlit as st
import serial
import sys
import time

arduino_activated = False

def write(data):
    #args_needed = 1
    ##data = args[0]
    #time.sleep(1)
    try:
        send = data.encode("utf-8")
        print(send)
        arduino.write(send)
        arduino.write(b'\n')
    except Exception as e:
        st.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

def read():
    time.sleep(1)
    return arduino.readline()
    
    try:
        with arduino.readline() as get:
            return get.decode('utf-8') 
    except:
        return None        
    

def init(userBaudrate="115200",count=1):
    global arduino
    global port_active
    args_needed = 1
    std_baudrate = ("300","1200","2400","4800","9600","14400","19200","28800","38400","57600","115200")

    for i in std_baudrate:
        if i == userBaudrate:
            baudrateOK=True
            break
        else:
            baudrateOK=False

    if not baudrateOK:
        print("BaudRate not in standard range.")
        print(f'Standard Baud Rates: {std_baudrate}')
        return
    
    arduino_ports = 'COM'
    for i in range(1,11,1):
        #print(arduino_ports+str(i))
        port_active = arduino_ports + str(i)
        try:
            with serial.Serial(port_active) as arduino: 
                arduino_activated = True
                break
        except serial.SerialException:
            arduino_activated = False
            continue;

    if not arduino_activated:
        print('No Arduino System Connected')
        return

    arduino = serial.Serial(port_active)
    arduino.baudrate=userBaudrate
    arduino.timeout=0.1
    arduino.parity='N'
    arduino.stopbits = 1
    arduino.bytesize = 8

    print(f'Arduino Connected at port {port_active}')
    print(f'BaudRate: {arduino.baudrate}')
    print(f'Timeout: {arduino.timeout}')
    print(f'Parity: {arduino.parity}')
    print(f'StopBits: {arduino.stopbits}')
    print(f'Bytesize: {arduino.bytesize}')
    return 

def close():
    if 'arduino' in globals():
        arduino.close()
    else:
        pass
        #print(globals())

def waitforRFID():
    if not arduino_activated:
        init()
    pass

def activeCOMS():
    activePorts = list()
    #activePorts.append('COM111')
    #activePorts.append('COM112')
    arduino_ports = 'COM'
    for i in range(1,11,1):
        #print(arduino_ports+str(i))
        port_active = arduino_ports + str(i)
        try:
            with serial.Serial(port_active) as arduino: 
                activePorts.append(port_active)
                break
        except serial.SerialException:
            continue;
    
    return activePorts

def ini(COMPort,userBaudrate='115200'):
    #std_baudrate = ("300","1200","2400","4800","9600","14400","19200","28800","38400","57600","115200")
    global arduino
    arduino = serial.Serial(COMPort,baudrate=userBaudrate)
    arduino.baudrate=userBaudrate
    arduino.timeout=0.1
    arduino.parity='N'
    arduino.stopbits = 1
    arduino.bytesize = 8
    #try:
    #    with serial.Serial(COMPort,baudrate=userBaudrate) as arduino:
    #        arduino.baudrate=userBaudrate
    #        arduino.timeout=0.1
    #        arduino.parity='N'
    #        arduino.stopbits = 1
    #        arduino.bytesize = 8
    #    return True
    #except:
    #    return False
    