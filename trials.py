from hardconnections import *
from IPython import embed
from threading import Timer
from tqdm import tqdm


# O2_buffer_toggle(p_opt=40,duration=10,toggletime=0.1)
# embed()


# # print("Wait time of 10 minutes")
# # time.sleep(10*60)

# loadlock_to_main_valve(False)
# embed()

#############################################################timer starts
total_time=600
bv_ll_toggletime=45
roughing_popt=0.02
t_n2_rough=60


t0=time.time()
timetoggle_buffer_to_loadlock_valve(toggletime=bv_ll_toggletime)

loadlock.log_serial_data(timeout=5)
p_init_loadlock=loadlock.read_last_entry() 

pfinal_N2=5*p_init_loadlock

t1=time.time()
t_rem=total_time- (t1-t0)
print("**********************")
print("Standby for automatic N2 quenching after {} seconds. Oxdn in process".format(t_rem-t_n2_rough))
print("Oxidation Pressure = {}".format(p_init_loadlock))
print("Final P to come after N2 purging = {}".format(pfinal_N2))
print("**********************")

t2=time.time()

if t_rem-t_n2_rough > 0:
    print("Oxidation in process")
    for i in tqdm(range(int(t_rem-t_n2_rough))):
        time.sleep(1)
else:
    print("Previous process got late. Initiating the next step")

N2_toggle(p_opt=pfinal_N2,duration=3,toggletime=0.1,initial_toggle=1.5)  

t3=time.time()      
t_rem=total_time - (t3-t0)

if t_rem >0:
    print("waiting for 1 minute N2 purge before roughing starts")
    for i in tqdm(range(int(t_rem))):
        time.sleep(1)
else:
    print("Previous process got late. Initiating the next step")

roughing_toggle(p_opt=roughing_popt, duration=5)
