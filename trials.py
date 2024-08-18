from hardconnections import *
from IPython import embed

from threading import Timer


# O2_buffer_toggle(p_opt=40,duration=10,toggletime=0.1)
# embed()


# # print("Wait time of 10 minutes")
# # time.sleep(10*60)

# loadlock_to_main_valve(False)
# embed()

#############################################################timer starts
total_time=600
roughing_popt=  0.02


# def initiate_oxidation(total_time):
t0=time.time()
timetoggle_buffer_to_loadlock_valve(toggletime=45)

#Noting the pressure valve
loadlock.log_serial_data(timeout=5)
p_init_loadlock=loadlock.read_last_entry() 

#setting the Final LL N2 charge pressure
p_N2_opt=5*p_init_loadlock

#Timing the N2 purging and Roughing process
t1=time.time()
t_rem=total_time- (t1-t0)

print("Standby for automatic N2 quenching after {} seconds. Oxdn in process".format(t_rem))
print("**********************")
print("Oxidation Pressure = {}".format(p_init_loadlock))
print("Final P to come after N2 purging = {}".format(p_N2_opt))

t2=time.time()
timer_N2charge=Timer(t_rem-60 , N2_toggle , [p_N2_opt,3,0.1,2]) #p_opt,duration=5,toggletime=0.1,initial_toggle=1.5
timer_roughing=Timer(t_rem , roughing_toggle,[roughing_popt,5,10])

timer_N2charge.start()
timer_roughing.start()



# OXDN 0:00. Total time = 600 sec. 
# t1=time.time()



# timetoggle_buffer_to_loadlock_valve(toggletime=4.5)
# print("Closing buffer")
# # t = Timer(10*60, roughing_toggle(p_opt=0.02,duration=5,toggletime=9))
# # t.start() 
# print("starting oxidation waittime")
# t2=time.time() #remaining time = 555 sec

# time.sleep(4.80)
# t3=time.time() #remaining time = 75 sec


# loadlock.log_serial_data(timeout=5)
# p_init_loadlock=loadlock.read_last_entry() 

# t4=time.time() #remaining time = 65 seconds

# p_n2_opt=5*p_init_loadlock
# N2_toggle(p_opt=p_n2_opt,toggletime=1,duration=5)
# t5=time.time()

# #START THE ROUGHING PUMP. (Time remaining  == 00)
# roughing_valve(True)
# roughing_toggle(p_opt=0.00000000001,duration=5,toggletime=10)
# roughing_valve(False)

