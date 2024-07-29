import notebook_utils as Q
import numpy as np
import time

#set all timescales in seconds
arduino=Q.ArduinoConnector('COM6')

buffervolume=Q.pgauge(name='buffervolume',port='COM5',relay_no=1)
mainchamber=Q.pgauge(name='mainchamber',port='COM7',relay_no=2)
loadlock=Q.pgauge(name='loadlock',port='COM4',relay_no=3)


def buffer_toggle(p_opt,duration=5,toggletime=0.1):
    '''inputs: p_opt, duration of logging after each toggle, and toggletime'''
    buffervolume.log_serial_data(timeout=duration)
    p_current= buffervolume.read_last_entry()
    thr=0.1
    p_max=760
    count=0
    if p_current >=p_max:
        print('ALERT: BUFFER PRESSURE REACHED MAXIMUM')
    else:    
        while p_opt-p_current>=thr:
            arduino.timetoggle_relay(buffervolume.relay_no,toggletime)
            time.sleep(1)
            buffervolume.log_serial_data(timeout=duration)
            p_current= buffervolume.read_last_entry()
            count+=1
            print("Toggle {count} copleted.")
        print("Final buffer presure = {p_current}. Toggling stopped after {counts} counts")



def mainchamber_toggle(p_opt,duration=5,toggletime=0.1):
    '''inputs: p_opt, duration of logging after each toggle, and toggletime'''
    mainchamber.log_serial_data(timeout=duration)
    p_current= mainchamber.read_last_entry()
    thr=0.01
    p_max=760
    count=0
    if p_current >=p_max:
        print('ALERT: MAINCHAMBER PRESSURE REACHED MAXIMUM')
    else:    
        while p_opt-p_current>=thr:
            arduino.timetoggle_relay(buffervolume.relay_no,toggletime)
            time.sleep(1)
            mainchamber.log_serial_data(timeout=duration)
            p_current= mainchamber.read_last_entry()
            count+=1
            print("Toggle {count} copleted.")
        print("Final mainchamber presure = {p_current}. Toggling stopped after {counts} counts")



def loadlock_toggle(p_opt,duration=5,toggletime=0.1):
    '''inputs: p_opt, duration of logging after each toggle, and toggletime'''
    loadlock.log_serial_data(timeout=duration)
    p_current= loadlock.read_last_entry()
    thr=0.1
    p_max=760
    count=0    
    if p_current >=p_max:
        print('ALERT: LOADLOCK PRESSURE REACHED MAXIMUM')
    else:
        while p_opt-p_current >=thr:
            print("p_current = {p_current}, togglecount = {count} \n")
            arduino.timetoggle_relay(loadlock.relay_no,toggletime)
            time.sleep(1)
            loadlock.log_serial_data(timeout=duration)
            p_current= loadlock.read_last_entry()
            count+=1
            print("Toggle {count} copleted.")
        print("Final loadlock presure = {p_current}. Toggling stopped after {counts} counts")


            
