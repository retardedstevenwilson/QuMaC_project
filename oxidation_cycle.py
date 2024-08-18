from hardconnections import *
from IPython import embed
from threading import Timer
from tqdm import tqdm


total_time=600
roughing_popt=0.02
t_n2_rough=60


def initiate_oxidation(total_time, pfinal_roughing, bv_ll_toggletime=45):
    
    t0=time.time()
    timetoggle_buffer_to_loadlock_valve(toggletime=bv_ll_toggletime)
    
    loadlock.log_serial_data(timeout=5)
    p_init_loadlock=loadlock.read_last_entry() 

    pfinal_N2=5*p_init_loadlock

    t1=time.time()
    t_rem=total_time- (t1-t0)
    print("**********************")
    print("Standby for automatic N2 quenching after {} seconds. Oxdn in process".format(t_rem))
    print("Oxidation Pressure = {}".format(p_init_loadlock))
    print("Final P to come after N2 purging = {}".format(pfinal_N2))
    print("**********************")
    
    t2=time.time()

    if t_rem-t_n2_rough > 0:
        print("Oxidation in process")
        for i in tqdm(range(t_rem-t_n2_rough)):
            time.sleep(1)
    else:
        print("Previous process got late. Initiating the next step")

    N2_toggle(p_opt=pfinal_N2,duration=3,toggletime=0.1,initial_toggle=1.5)  

    t3=time.time()      
    t_rem=total_time - (t3-t0)

    if t_rem >0:
        print("waiting for 1 minute N2 purge before roughing starts")
        for i in tqdm(range(t_rem)):
            time.sleep(1)
    else:
        print("Previous process got late. Initiating the next step")

    roughing_toggle(p_opt=pfinal_roughing, duration=5)

    # timer_N2charge=Timer(t_rem-60 , N2_toggle , [pfinal_N2,3,0.1,2]) #p_opt,duration=5,toggletime=0.1,initial_toggle=1.5
    # timer_roughing=Timer(t_rem , roughing_toggle,[pfinal_roughing,5,10])
    # timer_N2charge.start()
    # timer_roughing.start()


