# Codestone Conversion Simulator by Metamagic
# Trans rights are human rights ^^
# metty says hi

from random import randint
import sys
import math
import os
from threading import Thread
from threading import active_count
from threading import Lock
import time


class Results:
    def __init__(self):
        self.results = [0]*12
        #lv hp atk def agi
        self.stat_changes = [0]*5
    
    def __str__(self):
        return "Results: " + str(self.results) + "\nStats: " + str(self.stat_changes)
        
    def count(self):
        return sum(self.results)
    
    
lock = Lock()
progress = 0

n_updates = 5000

result_name = {
    0:'LVL -2',
    1:'Color Change',
    2:'HP +(2-5)',
    3:'Species Change',
    4:'Gender Change',
    5:'AGI +(2-3)',
    6:'STR +(2-3)',
    7:'LVL +2',
    8:'DEF +(2-3)',
    9:'STR -(2-3)',
    10:'AGI -(2-3)',
    11:'DEF -(2-3)'
}

result_odds = {
    0: 0.1348,
    1: 0.0674,
    2: 0.1348,
    3: 0.0337,
    4: 0.0787,
    5: 0.1124,
    6: 0.1124,
    7: 0.0562,
    8: 0.0562,
    9: 0.0562,
    10: 0.0787,
    11: 0.0787
}

def time_str(t):
    mod_t = t
    min = int(mod_t//60000)
    m_str = ""
    if min > 0: m_str = "{}m:".format(min)
    mod_t -= min*60000
    sec = int(mod_t//1000)
    s_str = ""
    if sec > 0: s_str = "{:02d}s:".format(sec)
    mod_t -= sec*1000
    return m_str+s_str+"{:03d}ms".format(int(mod_t))

def print_time(n, t):
    s = t/1000
    v = n/t
    #ms
    if(t < 1000):
        print(" - Performed {:,} simulations in %.3fms (%.3f/s)".format(n) % (t, v))
    #s
    elif t < 60*1000:
        print(" - Performed {:,} simulations in %.3fs (%.3f/s)".format(n) % (s, v))
    #min/s
    else:

        print(" - Performed {:,} simulations in %s (%.3f/s)".format(n) % (time_str(t), v))
        
        
def print_result(i, n, occ):
    name = result_name[i]
    occ_p = occ / n
    act_p = result_odds[i]
    p_diff = occ_p - act_p
    tab = "\t"
    if i != 3 and i != 4: tab = "\t\t"
    prefix = ""
    if occ_p > act_p: prefix = "+"
    print(" - %s%sx %d\t(%.3f%%, %s%.3f%% from %.3f%% avg.)" % (name, tab, occ, occ_p*100, prefix, p_diff*100, act_p*100))
        
def print_stat(i, n, avg):
    stat_type = ""
    match(i):
        case 0:
            stat_type = "LVL"
        case 1:
            stat_type = "HP"   
        case 2:
            stat_type = "STR"
        case 3:
            stat_type = "DEF"
        case 4:
            stat_type = "AGI"
            
    prefix = "+"
    if(n < 0): prefix = ""
    
    avg_str = ""
    if avg != 0: avg_str = "(%.3f per zap)" % avg
    
    print(" - %s:\t\t%s%d\t%s" % (stat_type, prefix, n, avg_str))
    
    
def print_simulation_results(res, n, n_thr, t):
    print("\n---Lab Ray Results:---")
    #time
    print_time(n,t)
    print(" - Threads used: %d" % n_thr)
        
    #stats
    print("\n**Stat Changes:**")
    for i in range(5):
        change = res.stat_changes[i]
        avg = change/n
        print_stat(i, change, avg)
        
    #results
    print("\n**Result Summary:**")
    for i in range(12):
        print_result(i, n, res.results[i])
    

def sim_zap(r):
    n = randint(1,89)
    if n <= 12:
        r.results[0] += 1
        r.stat_changes[0] -= 2
    #color
    elif n <= 18:
        r.results[1] += 1
    elif n <= 30:
        r.results[2] += 1
        r.stat_changes[1] += randint(2,5)
    #species
    elif n <= 33:
        r.results[3] += 1
    #gender
    elif n <= 40:
        r.results[4] += 1
    elif n <= 50:
        r.results[5] += 1
        r.stat_changes[4] += randint(2,3)
    elif n <= 60:
        r.results[6] += 1
        r.stat_changes[2] += randint(2,3)
    elif n <= 65:
        r.results[7] += 1
        r.stat_changes[0] += 2
    elif n <= 70:
        r.results[8] += 1
        r.stat_changes[3] += randint(2,3)
    elif n <= 75:
        r.results[9] += 1
        r.stat_changes[2] -= randint(2,3)
    elif n <= 82:
        r.results[10] += 1
        r.stat_changes[4] -= randint(2,3)
    elif n <= 89:
        r.results[11] += 1
        r.stat_changes[3] -= randint(2,3)
        
def thread_zap(t_res, i, n):
    global progress
    
    results = Results()
    interval = round(n / n_updates)
    last_j = 0
    
    #iterates n times
    for j in range(n):
        #progress bar
        if interval > 2 and j % interval == 0:
            lock.acquire()
            progress += j-last_j
            lock.release()
            last_j = j
        #simulation
        sim_zap(results)
    #saves results
    lock.acquire()
    progress += n - last_j
    t_res[i] = results
    lock.release()


def main():    
    n = 1000 #default
    
    if len(sys.argv) > 2:
        print("Error: Too many arguments!")
        quit()
    elif len(sys.argv) == 2:
        if not sys.argv[1].isdigit():
            print("Error: Argument must be integer!")
            quit()
        else:
            n = int(sys.argv[1])
            
    tallied_results = Results()
    
    start_t = time.time()
    n_threads = os.cpu_count()
    n_count = [0]*n_threads
    
    #divides n into threads
    for x in range(n_threads):
        n_count[x] = n // n_threads + (1 if x < (n % n_threads) else 0)
        
        
    print("Performing lab ray simulation for " + str(n) + " occurrences:")
    print("Torturing lab rat using %d threads..." % n_threads)
    
    #starts and runs threads
    i = 0
    t_res = [None] * n_threads
    print("Progress: Thread 0/%d started." % (n_threads), end='\r')
    for num in n_count:
        t = Thread(target=thread_zap, args=[t_res, i, num])
        t.start()
        print("Progress: Thread %d/%d started." % ((i+1), n_threads), end='\r')
        i += 1
    print("Progress: All %d threads started. Running calculations..." % (n_threads))
    
    #progress loop
    last_count = -1
    last_t = -1
    working = True
    while(working):
        nt = active_count()
        if nt == 1: working = False
        if progress - last_count > n / (n_updates/10):
            print("Progress: %.3f%% (Time Elapsed: %s)" % ((progress/n)*100, time_str((time.time()-start_t)*1000)), end= '\r')
    print("Progress: Simulation complete. Printing results...")
    
    #sums results
    f_res = Results()
    for res in t_res:
        for i in range(12):
            f_res.results[i] += res.results[i]
        for i in range(5):
            f_res.stat_changes[i] += res.stat_changes[i]
    
    t = (time.time() - start_t) * 1000
    print_simulation_results(f_res, n, n_threads, t)
    
    
main()