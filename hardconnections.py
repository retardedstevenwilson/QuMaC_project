import notebook_utils as Q
import numpy as np
import time

#set all timescales in seconds
arduino=Q.ArduinoConnector('COM6')


O2_relay=4
N2_relay=3
buffer_to_main_valve_relay=2
roughing_relay=1

buffervolume=Q.pgauge(name='buffervolume',port='COM5')
mainchamber=Q.pgauge(name='mainchamber',port='COM7')
loadlock=Q.pgauge(name='loadlock',port='COM4')


def O2_buffer_toggle(p_opt,duration=10,toggletime=0.1):
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



# def mainchamber_toggle(p_opt,duration=5,toggletime=0.1):
#     '''inputs: p_opt, duration of logging after each toggle, and toggletime'''
#     mainchamber.log_serial_data(timeout=duration)
#     p_current= mainchamber.read_last_entry()
#     thr=0.01
#     p_max=760
#     count=0
#     if p_current >=p_max:
#         print('ALERT: MAINCHAMBER PRESSURE REACHED MAXIMUM')
#     else:    
#         while p_opt-p_current>=thr:
#             arduino.timetoggle_relay(buffervolume.relay_no,toggletime)
#             time.sleep(1)
#             mainchamber.log_serial_data(timeout=duration)
#             p_current= mainchamber.read_last_entry()
#             count+=1
#             print("Toggle {count} copleted.")
#         print("Final mainchamber presure = {p_current}. Toggling stopped after {counts} counts")



# def loadlock_toggle(p_opt,duration=5,toggletime=0.1):
#     '''inputs: p_opt, duration of logging after each toggle, and toggletime'''
#     loadlock.log_serial_data(timeout=duration)
#     p_current= loadlock.read_last_entry()
#     thr=0.1
#     p_max=760
#     count=0    
#     if p_current >=p_max:
#         print('ALERT: LOADLOCK PRESSURE REACHED MAXIMUM')
#     else:
#         while p_opt-p_current >=thr:
#             print("p_current = {p_current}, togglecount = {count} \n")
#             arduino.timetoggle_relay(loadlock.relay_no,toggletime)
#             time.sleep(1)
#             loadlock.log_serial_data(timeout=duration)
#             p_current= loadlock.read_last_entry()
#             count+=1
#             print("Toggle {count} copleted.")
#         print("Final loadlock presure = {p_current}. Toggling stopped after {counts} counts")


def open_buffer(duration):
    arduino.timetoggle_relay(buffer_to_main_valve_relay,duration=duration)


            
def N2_toggle(p_opt,duration=10,toggletime=0.1):

    mainchamber.log_serial_data(timeout=5)
    p_current= mainchamber.read_last_entry()
    thr=0.1
    # p_max=760
    # if p_current >=p_max:
    #     print('ALERT: MAINCHAMBER PRESSURE REACHED MAXIMUM')
    # else:
    count=0    
    try:
        while p_opt-p_current>=thr:
            arduino.timetoggle_relay(N2_relay,toggletime)
            time.sleep(1)
            mainchamber.log_serial_data(timeout=duration)
            p_current= mainchamber.read_last_entry()
            print("current p = ",p_current)
            count+=1
            print("Toggle {} completed. Waiting 5 seconds for stabilization".format(count))
            time.sleep(5)
    except KeyboardInterrupt:
        print("Toggle process manually stopped")
    print("Final mainchamber presure = {}. Toggling stopped after {} counts".format(p_current,count))


def roughing_toggle(p_opt,duration=5,toggletime=10):
    mainchamber.log_serial_data(timeout=5)
    p_current= mainchamber.read_last_entry()
    count=0    
    thr=0.1
    try:
        while p_current - p_opt >= thr:
            arduino.timetoggle_relay(roughing_relay,toggletime)
            time.sleep(2)
            mainchamber.log_serial_data(timeout=duration)
            p_current= mainchamber.read_last_entry()
            print("current p = ",p_current)
            count+=1
            print("Toggle {} completed. Waiting 5 seconds for stabilization".format(count))
            time.sleep(5)
    except KeyboardInterrupt:
        print("Toggle process manually stopped")
    print("Final mainchamber presure = {}. Toggling stopped after {} counts".format(p_current,count))
