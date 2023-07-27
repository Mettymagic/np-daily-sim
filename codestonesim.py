# Codestone Conversion Simulator by Metamagic
# Trans rights are human rights ^^
# metty says hi

import random
import sys
import math

tan_values = {
    0:("Zei",3550),
    1:("Tai-Kai",3500),
    2:("Vo",3700),
    3:("Orn",3500),
    4:("Mau",4000),
    5:("Main",2500),
    6:("Lu",9000),
    7:("Har",4200),
    8:("Eo",19000),
    9:("Bri",2300)
}

red_values = {
    0:("Cui",45000),
    1:("Kew",70000),
    2:("Mag",18600),
    3:("Sho",19800),
    4:("Vux",46000),
    5:("Zed",62500)
}

def print_stat(i, n):
    stat_type = ""
    match(i):
        case 0:
            stat_type = "LVL"
        case 1:
            stat_type = "HP"   
        case 2:
            stat_type = "ATK"
        case 3:
            stat_type = "DEF"
        case 4:
            stat_type = "AGI"
            
    prefix = "+"
    if(n < 0): prefix = ""
    print(" * %s: %s%d" % (stat_type, prefix, n))
    
#prints the results by number, result, and count
#summarizes random results per category
def print_simulation_results(n, profit, num_tan, num_red):
    
    print("**Results:**                \n")
    
    to_print.append("  * LVL: +%d (%d -> %d)" % (stat_diff[0], start_stats[0], end_stats[0]))
    
    comp_val = compress_np_value(abs(profit))
    if profit > 0:
        print("Profit! +" + comp_val + " ( +{:,d}np )".format(profit))
    elif profit < 0:
        print("Loss! -" + comp_val + " ( -{:,d}np )".format(abs(profit)))
    else:
        print("No gain or loss! ( 0np )")
        
    avg_profit = float(profit) / n
    print("Average np gain/loss: %.2fnp" % (avg_profit))

    print("\n--Tan Codestones Used:--")
    for i in range(0,10):
        amt = num_tan[i]
        percent = (amt / (10*n)) * 100
        if amt > 0:
            name = tan_values[i][0]
            price = tan_values[i][1]
            print("  * %s x %d ( %.2f%% )\n      Cost: {:,d}np ( {:,d}np x %d )".format(price*amt, price) % (name, amt, percent, amt))
    
    print("\n--Red Codestones Gained--")
    for i in range(0,6):
        amt = num_red[i]
        percent = (amt / n) * 100
        if amt > 0:
            name = red_values[i][0]
            price = red_values[i][1]
            print("  * %s x %d ( %.2f%% )\n      Cost: {:,d}np ( {:,d}np x %d )".format(price*amt, price) % (name, amt, percent, amt))
            
#works only with positive numbers (eg abs(x))
def compress_np_value(np):
    bils = np // 1000000000
    np -= bils * 1000000000
    
    mils = np // 1000000
    np -= mils * 1000000
    
    kilos = np // 1000
    np -= kilos * 1000
    
    str = ""
    if bils > 0:
        str = "{}.{:03d}bil np".format(bils, mils)
    elif mils > 0:
        str = "{}.{:03d}mil bp".format(mils, kilos)
    elif kilos > 0:
        str = "{}.{:03d}k np".format(kilos, np)
    else:
        str = "{}np".format(np)
    return str
    
#simulates the daily by generating random numbers to obtain result
def simulate_volcano(profit, num_tan, num_red):
    #pay 10 tan codestones
    price = 0
    for i in range(10):
        cs = random.randint(0,9)
        price += tan_values[cs][1]
        num_tan[cs] += 1
        
    #get 1 red codestone
    r_cs = random.randint(0,5)
    num_red[r_cs] += 1
    value = red_values[r_cs][1]
    
    #return profit
    return value - price

    
#track_stats is an optimization that skips certain stat checks if they aren't needed
def main():
    n = 100000
    profit = 0
    num_tan = [0,0,0,0,0,0,0,0,0,0]
    num_red = [0,0,0,0,0,0]
    
    if len(sys.argv) > 2:
        print("Error: Too many arguments!")
        quit()
    elif len(sys.argv) == 2:
        if not sys.argv[1].isdigit():
            print("Error: Argument must be integer!")
            quit()
        else:
            n = int(sys.argv[1])
            
    print("Performing codestone volcano simulation for " + str(n) + " occurrences:")
    print("Chucking codestones into the volcano...")
    
    update_interval = n / 1000
    
    for i in range(n):
        #progress bar
        if update_interval > 0:
            if i % update_interval == 0:
                perc = (i/n)*100
                print("Progress: %.1f%%" % (perc), end= '\r') 
        
        #adds results
        profit += simulate_volcano(profit, num_tan, num_red)
        
    
    print_simulation_results(n, profit, num_tan, num_red)

main()