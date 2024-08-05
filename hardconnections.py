import notebook_utils as Q
import numpy as np
import time

#set all timescales in seconds
arduino=Q.ArduinoConnector('COM6')

roughing_relay=1
buffer_to_loadlock_relay=2
N2_relay=3
O2_relay=4
loadlock_to_main_relay=5

buffervolume=Q.pgauge(name='buffervolume',port='COM3') #change comport to 5 for madhavi's laptop
mainchamber=Q.pgauge(name='mainchamber',port='COM7')
loadlock=Q.pgauge(name='loadlock',port='COM4')


def loadlock_to_main_valve(value):
    arduino.toggle_relay(loadlock_to_main_relay,state=value)

def roughing_valve(value):
    arduino.toggle_relay(roughing_relay,state=value)


def timetoggle_buffer_to_loadlock_valve(toggletime):
    arduino.timetoggle_relay(buffer_to_loadlock_relay,toggletime=toggletime)


def O2_buffer_toggle(p_opt,duration=10,toggletime=0.1):
    print("Starting O2 toggle")
    '''inputs: p_opt, duration of logging after each toggle, and toggletime'''
    buffervolume.log_serial_data(timeout=5)
    p_current= buffervolume.read_last_entry()
    thr=0.1
    p_max=760
    if p_current >=p_max:
        print('ALERT: BUFFER PRESSURE REACHED MAXIMUM')
    else:
        count=0    
        try:
            while p_opt-p_current>=thr:
                arduino.timetoggle_relay(O2_relay,toggletime)
                time.sleep(1)
                buffervolume.log_serial_data(timeout=duration)
                p_current= buffervolume.read_last_entry()
                print("current p = ",p_current)
                count+=1
                print("Toggle {} completed.".format(count))
                time.sleep(5)
        except KeyboardInterrupt:
            print("Toggle process manually stopped")
        print("Final buffer presure = {}. Toggling stopped after {} counts".format(p_current,count))


            
def N2_toggle(p_opt,duration=5,toggletime=0.1,initial_toggle=1.5):
    '''N2 Charging in the loadlock'''
    print("Starting N2 toggle")
    arduino.timetoggle_relay(N2_relay,toggletime=initial_toggle)
    loadlock.log_serial_data(timeout=5)
    p_current= loadlock.read_last_entry()
    
    thr=0.1*p_opt
    count=0

    try:
        while p_opt-p_current>=thr:
            arduino.timetoggle_relay(N2_relay,toggletime)
            time.sleep(1)
            loadlock.log_serial_data(timeout=duration)
            p_current= loadlock.read_last_entry()
            print("current p = ",p_current)
            count+=1
            print("Toggle {} completed. Waiting 5 seconds for stabilization".format(count))
            time.sleep(5)
            print("Final mainchamber presure = {}. Toggling stopped after {} counts".format(p_current,count))
    except KeyboardInterrupt:
        print("Toggle process manually stopped")


def roughing_toggle(p_opt,duration=5,toggletime=10):
    '''Starts roughing process in the loadlock'''
    thr=0.1*p_opt
    print("Starting roughing toggle. Opening the valve")
    roughing_valve(True)

    try:
        loadlock.log_serial_data(timeout=5)
        p_current= loadlock.read_last_entry()
        
        arduino.toggle_relay(roughing_relay,True)
        
        while p_current - p_opt >= thr:
            loadlock.log_serial_data(timeout=duration)
            time.sleep(1)
            p_current= loadlock.read_last_entry()
            print("current p = {}. Roughing continues... ".format(p_current))
            time.sleep(1)
        
        print("Optimum P reached. Turning off the roughing relay")
        arduino.toggle_relay(roughing_relay,False)
    
    except KeyboardInterrupt:
        print("Roughing toggle manually stopped")
        arduino.toggle_relay(roughing_relay,False)
        
    print("Final mainchamber presure = {}".format(p_current))
    