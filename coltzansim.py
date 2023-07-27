# Coltzan's Shrine Simulator by Metamagic
# Trans rights are human rights ^^
# metty says hi

import random
import sys
import functools
import math
import getopt
import random

#used to make sorting easier
stats_res = (18, 26, 30, 42, 34, 38, 41, 45, 49, 53)
maybe_stats_res = (5, 6, 7, 8, 9, 13, 16, 19, 21, 23, 32)
smallmoney_res = (56, 59)
bigmoney_res = (51, 52, 54, 55, 57, 58)

#note: prizes infer pet has lvl > 100 and str/agi/def > 50
prize_table = {
    1: (), #nothing
    2: (), #nothing
    3: ("burnt food", -1), #burnt food
    4: (), #heal all pets
    5: ("desert food", -1), #desert food
    6: ("+1 str",-1), #1 str
    7: ("+1 lvl",-1), #1 lv
    8: ("+1 agi",-1), #1 agi
    9: ("+1 def",-1), #1 def
    10: (), #heal all pets
    11: (), #random np value
    12: (), #heal all pets
    13: ("+1 lvl",-1), #1 lv
    14: ("one dubloon coin", 1000),
    15: ("dusty tome", -1), #1 book
    16: ("+1 def",-1), #1 def
    17: ("two dubloon coin", 1500),
    18: ("+1 int", -1),
    19: ("+1 agi",-1), #1 agi
    20: ("serf lens", 1),
    21: ("+1 lvl", -1), #1 lv
    22: ("coltzans gem", 1),
    23: ("+1-3 str", -1), #1-3 str
    24: ("stone shield",1),
    25: ("10 dubloon coin", 6500),
    26: ("+1-2 int", -1),
    27: ("royal scarabug",4),
    28: ("sutekh plushie",1),
    29: ("expert lens", 2),
    30: ("+1-3 int", -1),
    31: ("coltzans burning gem", 5),
    32: ("+1 lvl", -1), #1 lv
    33: ("king coltzan coin", 95),
    34: ("+1-3 str", -1),
    35: ("artisans lens", 200),
    36: ("coltzans ring", 50),
    37: ("twenty dubloon coin", 13000),
    38: ("+1-6 move", -1),
    39: ("coltzans shrine coin", 35000),
    40: ("royal wadjet",3000),
    41: ("+1-6 def", -1),
    42: ("+1-6 int", -1),
    43: ("sand ball",200),
    44: ("coltzans necklace", 6000),
    45: ("+1-6 str",-1),
    46: ("craftsmens lens", 73000),
    47: ("fifty dubloon coin", 34300),
    48: ("knights shield",9000),
    49: ("+1-2 lvl", -1),
    50: ("princely lens", 88000),
    51: ("coltzans diadem", -2),
    52: ("kings lens", 100000000),
    53: ("+1-3 lvl",-1),
    54: ("princely shield", -2),
    55: ("coltzans sceptre", -2),
    56: ("500,000 np", 500000),
    57: ("kings shield", -2),
    58: ("kings shield + 1mil np", -2),
    59: ("1,000,000 np", 1000000)
}

#going off of neo_truth's item list and not jellyneo's
#for result 15
books = {
    0: ("deserted desert scroll", 14),
    1: ("coltzans last words", 2),
    2: ("ringed scroll", 7),
    3: ("a history of the lost desert", 2),
    4: ("lost desert architecture", 85),
    5: ("ancient scarab scroll", 1)
}

#going off of neo_truth's item list and not jellyneo's
#for result 3
burnt_foods = {
    0: ("broken corn pyramid", 2),
    1: ("toasted pyramibread", 50),
    2: ("scorched sutek muffin", 30),
    3: ("scorched tut trout", 18),
    4: ("scorched pyramicake", 40),
    5: ("spoiled sphynx links", 30),
    6: ("rotten puntec fruit", 25),
    7: ("damaged bagguss", 30),
    8: ("mangled geopeppers", 40),
    9: ("ruined ptolymelon", 30),
    10: ("scorched suti fruit", 100),
    11: ("scorched chomato", 70),
    12: ("scorched gobi fruit", 95),
    13: ("scorched pleto", 30),
    14: ("scorched rhuby", 300),
    15: ("scorched cheopple", 380),
    16: ("burnt vinegar dipped kabob", 13),
    17: ("zonutuk fruit bowl", 8),
    18: ("sand dabs", 7)
}

#going off of neo_truth's item list and not jellyneo's
#for result 5
desert_foods = {
    0: ("grackle bug on a stick", 100),
    1: ("grackle-stuffed turkey", 280),
    2: ("cheops plant", 350),
    3: ("ummagine", 30),
    4: ("sutek muffin", 100),
    5: ("mummified pepper", 95),
    6: ("tchea fruit", 1),
    7: ("sphinx links", 200),
    8: ("pyramibread", 130),
    9: ("pyramicake", 120),
    10: ("cheopple", 20),
    11: ("pleto melon", 13),
    12: ("gobi fruit", 45),
    13: ("chomato", 15),
    14: ("suti fruit", 15),
    15: ("rhuby fruit", 10),
    16: ("desert kabob", 50)
}


#for some of the crazy rare stuff
rare_est_prices = { 51: 15000000, 54: 50000000, 55: 600000000 }

#modifier associated with each hour
hr_boost = {
    0:6,
    1:5,2:5,
    3:4,4:4,
    5:3,6:3,
    7:2,8:2,
    9:1,10:1,
    11:0,12:0,13:0,
    14:1,15:1,
    16:2,17:2,
    18:3,19:3,
    20:4,21:4,
    22:5,23:5
}

#optimization for counting results, used for parsing
def res_count(n, list):
    count = 0
    for l in list:
        if l[0] == n: count += 1
        if l[0] > n: break
    return count
    
def maybe_res_count(n, list):
    stat_c = 0
    noth_c = 0
    for l in list:
        if l[0] == n: 
            if l[1]: stat_c += 1
            else: noth_c += 1
        if l[0] > n: break
    return stat_c,noth_c
    
    
#([(num, count),...], ... )
#sorts the results by category and occurences
def parse_results(results):
    sorted_results = sorted(results, key=lambda l: l[0])
    
    crud = []
    stats = []
    maybe_stats = []
    smallmoney = []
    bigmoney = []
    
    n = len(sorted_results)
    update_interval = round(n / 1000)
    
    line_num = 0
    for res in sorted_results:
        if(update_interval > 0):
            if line_num % update_interval == 0:
                perc = (line_num/n)*100
                print("Progress: %.1f%%" % (perc), end= '\r') 
            
        if stats_res.count(res[0]) > 0:
            stats.append(res)
            
        elif maybe_stats_res.count(res[0]) > 0:
            maybe_stats.append(res)
            
        elif smallmoney_res.count(res[0]) > 0:
            smallmoney.append(res)
            
        elif bigmoney_res.count(res[0]) > 0:
            bigmoney.append(res)
        
        else:
            crud.append(res)
        
        line_num += 1
            
    print("Sorting completed. Compressing results...")
    # crud, stats, maybestats, smallmoney, bigmoney
    lists = ([], [], [], [])
            
    for i in range(1, 60):
        print(("Compressing result " + str(i) + " / 59"), end= '\r') 
        #stats
        if i in stats_res:
            x = res_count(i, stats)
            if x > 0: lists[1].append((i, x))
        #maybe-stats are separated into stats and nothing
        elif i in maybe_stats_res:
            stat_c,noth_c = maybe_res_count(i, maybe_stats)
            if stat_c > 0: lists[1].append((i, stat_c))
            if noth_c > 0: lists[0].append((i, stat_c))
        #small money
        elif i in smallmoney_res:
            a = res_count(i, smallmoney)
            if a > 0: lists[2].append((i, a))
        #big money
        elif i in bigmoney_res:
            b = res_count(i, bigmoney)
            if b > 0: lists[3].append((i, b))
        #crud
        else:
            q = res_count(i, crud)
            if q > 0: lists[0].append((i, q))
            
    print("Compression completed, summing and printing results...")
    
    return lists
            
            
#used to tally total results in each section
def simplify_map_results(l):
    return l[1]
def reduce_results(a, b):
    return a+b
    

def get_maybe_stats(num):
    inc = 0
    nothing = 0
    if len(num) > 1:
        if num[1] == True: inc += 1
        else: nothing += 1
    return (inc,nothing)
    
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
        str = "{}.{}bil np".format(bils, round(mils/100))
    elif mils > 0:
        str = "{}.{}mil np".format(mils, round(kilos/100))
    elif kilos > 9:
        str = "{}.{}k np".format(kilos, round(np/100))
    else:
        str = "{}np".format(np + kilos*1000)
    return str

def print_item_lookup(lookup, count, nesting = 0, total = -1, n = -1):
    name = lookup[0]
    item_price = lookup[1]
    total_value = item_price * count
        
    #nesting level
    indent = " " * nesting
    if(nesting > 0): indent += "* "
    
    #result number
    prefix = ""
    if n > 0: prefix = str(n) + ": "
    
    #item name and number
    item_str = "%s x %d " % (name, count)
    
    #shows percentage
    p_str = ""
    if total > 0: p_str = "(%.2f%%) " % (count / total * 100)
    
    #price or estimated price
    value = ""
    if item_price == -2:
        est_price = rare_est_price[n]
        str_value = compress_np_value(est_price)
        value = "--> Unpriced (Est. " + str_value + ") x " + str(count) + " "   
    elif item_price > -1:
        str_value = compress_np_value(item_price)
        total_str_value = compress_np_value(item_price * count)
        value = "--> %s (%s x %d) " % (total_str_value, str_value, count)
        
    return indent + prefix + item_str + p_str + value

def process_result(res, total):
    num = res[0]
    lookup = prize_table[num]
    if len(lookup) > 0:
        count = res[1]
        return print_item_lookup(lookup, count, 2, total=total, n=num)
    return "ERROR - empty lookup?"

def process_statistics(np, n, est_15_days, stat_diff, total_stat_diff):
    to_print = []
    to_print.append("\n|| Statistics: ||")
    to_print.append(" Number of shrine visits: %d" % (n))
    to_print.append("  * Number of visits on the 15th day: %d" % (est_15_days))
    to_print.append(" Total NP earned: %s ( {:,d}np )".format(np) % (compress_np_value(np)))
    to_print.append("  * Average NP earned per visit: %dnp" % (round(np / n)))
    to_print.append(" Average INT earned per visit: %.3f" % (stat_diff[0] / n) )
    to_print.append(" Average stats (not incl. INT) earned per visit: %.3f" % ((total_stat_diff-stat_diff[0]) / n) )
    
    return to_print
    
    
def process_jackpot_results(big, huge, n):
    to_print = []
    np = 0
    
    if len(huge) > 0: 
        total = functools.reduce(reduce_results, map(simplify_map_results, huge))
        to_print.append("\n!!!!!HOLY FUCKING SHIT!!!!!")
        for res in huge:
            num = res[0]
            lookup = prize_table[num]
            if len(lookup) > 0:
                count = res[1]
                if lookup[1] > 0:
                    np += lookup[1] * count
                elif lookup[1] == -2:
                    np += rare_est_price[num] * count
            to_print.append(process_result(res, -1))
    
    if len(big) > 0:
        total = functools.reduce(reduce_results, map(simplify_map_results, big))
        to_print.append("\n!!!JACKPOT!!!")
        for res in big:
            num = res[0]
            count = res[1]
            np += prize_table[num][1] * count
            to_print.append(process_result(res, -1))
    
    return to_print,np
    
def process_stat_results(results, n, start_stats, end_stats):
    total = functools.reduce(reduce_results, map(simplify_map_results, results))
    total_stat_diff = 0
    stat_diff = [0] * 5
    for i in range(5): 
        change = end_stats[i]-start_stats[i]
        stat_diff[i] = change
        total_stat_diff += change
        
    to_print = []

    to_print.append("\n**Stat Results**")
    to_print.append("*Number of Results:* %d ( %.2f%% )" % (total, (total / n) * 100))
    for res in results:
        to_print.append(process_result(res, total))
        
    #shows total stat changes
    to_print.append("*Total Stat Changes:* %d (%d incl. INT)" % (total_stat_diff-stat_diff[0], total_stat_diff))
    to_print.append("  * INT: +%d (%d -> %d)" % (stat_diff[0], start_stats[0], end_stats[0]))
    to_print.append("  * LVL: +%d (%d -> %d)" % (stat_diff[1], start_stats[1], end_stats[1]))
    to_print.append("  * STR: +%d (%d -> %d)" % (stat_diff[2], start_stats[2], end_stats[2]))
    to_print.append("  * DEF: +%d (%d -> %d)" % (stat_diff[3], start_stats[3], end_stats[3]))
    to_print.append("  * AGI: +%d (%d -> %d)" % (stat_diff[4], start_stats[4], end_stats[4]))
    
    return to_print,stat_diff,total_stat_diff

#adds a sublist to the str_list to be printed
def print_crud_sublist(str_list, n, count):
    #burnt food
    if n == 3:
        items = [0] * len(burnt_foods)
        #get random items
        for i in range(count):
            r = random.randint(0, len(burnt_foods)-1)
            items[r] += 1
        #prints items
        j = 0
        for food_c in items:
            str_list.append(print_item_lookup(burnt_foods[j], items[j], 4, count))
            j += 1
            
    #desert food
    elif n == 5:
        items = [0] * len(desert_foods)
        #get random items
        for i in range(count):
            r = random.randint(0, len(desert_foods)-1)
            items[r] += 1
        #prints items
        j = 0
        for food_c in items:
            str_list.append(print_item_lookup(desert_foods[j], items[j], 4, count))
            j += 1
    #books
    elif n == 15:
        items = [0] * len(books)
        #get random items
        for i in range(count):
            r = random.randint(0, len(books)-1)
            items[r] += 1
        #prints items
        j = 0
        for food_c in items:
            str_list.append(print_item_lookup(books[j], items[j], 4, count))
            j += 1

#for result 11
def est_randnp(count):
    n = 0
    for i in range(count): n += random.randint(1,400)
    return n

#gets a string of the lines to be printed for the crud results
def process_crud_results(results, n):
    nothing = []
    heal = []
    np = 0
    str_list = []
    total = functools.reduce(reduce_results, map(simplify_map_results, results))
  
    for res in results:
        num = res[0]
        count = res[1]
        
        #adds to nothing count
        if num in maybe_stats_res or num < 3:
            nothing.append(res)
            continue
        #adds to heal count
        elif num in (4, 10, 12):
            heal.append(res)
            continue
        #does random np line
        elif num == 11:
            est_np = est_randnp(count)
            np_11 = compress_np_value(est_np)
            str_list.append("  * 11: 1-400np x %d --> %s " % (count,np_11))
            np += est_np
            continue
        
        #adds to total np count
        lookup = prize_table[num]
        if len(lookup) > 0:
            if lookup[1] > 0:
                np += lookup[1] * res[1]
                
        #get print line
        str_list.append(process_result(res, total))
        
        #get item lists
        if num in (3, 5, 15):
            print_crud_sublist(str_list, num, count)
            
    if len(heal) > 0:
        str_list.append("  * heal all pets")
        n_list = "    * "
        for r in heal:
            if r[1] > 0:
                n_list += "%d: x%d, " % (r[0],r[1])
        str_list.append(n_list[:-2])
    if len(nothing) > 0:
        str_list.append("  * nothing :(")
        n_list = "    * "
        for r in nothing:
            if r[1] > 0:
                n_list += "%d: x%d, " % (r[0],r[1])
        str_list.append(n_list[:-2])
           
    str_list.insert(0, "-Total Value:- %s ( {:,d} )".format(np) % (compress_np_value(np)))
    str_list.insert(0, "-Number of Results:- %d ( %.2f%% )" % (total, (total/n)*100))
    str_list.insert(0, "\n--Reward Results--")
    
    return str_list,np

    
#prints the results by number, result, and count
#summarizes random results per category
#results in format (n, count)
def print_simulation_results(results, n, est_15_days, start_stats, end_stats):
    np = 0
    stat_diff = [0]*5
    total_stat_diff = 0
    #jackpots
    if len(results[2]) + len(results[3]) > 0: 
        jackpot_lines,jackpot_np = process_jackpot_results(results[2], results[3], n)
        np += jackpot_np
        for line in jackpot_lines:
            print(line)
    #stats
    if len(results[1]) > 0: 
        stat_lines,changed_stats,total_change = process_stat_results(results[1], n, start_stats, end_stats)
        stat_diff = changed_stats
        total_stat_diff = total_change
        for line in stat_lines:
            print(line)
    #crud
    if len(results[0]) > 0:     
        crud_lines,crud_np = process_crud_results(results[0], n)
        np += crud_np
        for line in crud_lines:
            print(line)
    #statistics
    statistics_lines = process_statistics(np, n, est_15_days, stat_diff, total_stat_diff)
    for line in statistics_lines:
        print(line)

#simulates the daily by generating random numbers to obtain result number
#assumes all factors that can be maxed are (200+ intel, 00:xx:xx NST, hp <= 10)
#roughly estimates the 15th day bonus knowing there are 12 15th days in a year (365 days)
# [result, base, intel, hr, hp, rbase, day15]
def simulate_coltan(isDay15, isLowHP, hr, intel):
    base = random.randint(1,7)
    hp = 0
    if(isLowHP): hp = random.randint(1,5)
    rbase = [0,0,0]
    for x in rbase:
        if random.randint(1,6) == 1:
            rbase[x] = random.randint(1,12)
    day15 = 0
    if isDay15 and random.randint(1,5) == 1:
        day15 += random.randint(1,12)
    
    result = base+intel+hr+hp+rbase[0]+rbase[1]+rbase[2]+day15
    return result#, base, intel, hr, hp, rbase, day15)
    

#main function that runs the program
#accepts command line input for # of days to run, defaults to 365 (1 year)
# -h, --help, --args specifies command arguments
# --stats=<int,lv,str,def,agi> specifies all of pets starting stats. all 5 must be specified.
# default: 201,101,51,51,51
# --hp=<number between 0 and 1> specifies the ratio at which low-hp boost is applied
# default: 1
# --hr=<number between 0 and 23> specifies the time used to get results
# default: 0
# --hr2=<number between 0 and 1>%<number between 0 and 23> specifies a percentage of the time in which a second time should be used
# eg --hr2=0.25%23 means 23:xx:xx NST will be used for 25% of the results
# default: none

#the neo_truths post doesnt specify whether these are inclusive values or not so i assume they are
def get_int_boost(int):
    if(int >= 200): return 6
    elif(int >= 175): return 5
    elif(int >= 140): return 4
    elif(int >= 95): return 3
    elif(int >= 75): return 2
    elif(int >= 40): return 1
    else: return 0

#prints argument help
def print_help():
    print("**Argument Usage**")
    print("-h, --help, --args specifies command arguments")
    print("--stats=<int,lv,str,def,agi> specifies all of pets starting stats. all 5 must be specified.")
    print(" * default: 201,101,51,51,51")
    print("--hp=<number between 0 and 1> specifies the ratio at which low-hp boost is applied")
    print(" * default: 1")
    print("--hr=<number between 0 and 23> specifies the time used to get results")
    print(" * default: 0")
    print("--hr2=<number between 0 and 1>%<number between 0 and 23> specifies a percentage of the time in which a second time should be used")
    print(" * eg --hr2=0.25%23 means 23:xx:xx NST will be used for 25% of the results")
    print(" * default: none")
    
def exit_program():
    print("")
    print_help()
    quit()

    
#interprets any provided arguments or returns the default (default = max)
def parse_args():
    #default args
    n = 365 # number of occurrences to simulate
    stats=[201, 101, 51, 51, 51] # pet stats
        # int, lv, str, def, agi
    hp = 1.0 # ratio of low-hp boosts
    hr = 0 # hour
    hr2 = 1 # second hour boost
    hr2_ratio = 0.0 # ratio of second hour boost
    
    #reads args
    got_n = False
    optlist, args = getopt.getopt(sys.argv[1:], "hn:", ["help", "args", "num=", "stats=", "hr=", "hr2=", "hp="])

    for opt, val in optlist:
        #help command
        if opt in ("--help", "--args", "-h"): 
            exit_program()

        elif opt in ("-n", "--num"):
            if not val.isdigit():
                print("error in " + opt + " argument: " + val + " is not an integer!")
                exit_program()
            elif int(val) < 1:
                print("error in " + opt + " argument: " + val  + " must be greater than 1!")
                exit_program()
            n = int(val)
            got_n = True
        
        #stats command
        elif opt == '--stats':
            arr = val.split(",")
            if len(arr) != 5:
                print("error in --stats= argument: there must be 5 arguments!")
                exit_program()
            num = 0
            for stat in arr:
                if not stat.isdigit():
                    print("error in --stats= argument: " + stat + " is not an integer!")
                    exit_program()
                
                #checks for errors in stats
                if int(stat) > 0 or (num == 0 and int(stat) == 0): 
                    stats[num] = int(stat)
                else:
                    print("error in --stats= stat: " + i + " is not greater than 0! (though int can be 0)")
                    exit_program()
                num += 1
        
        #health ratio command
        elif opt == '--hp':
            if not val.isfloat():
                print("error in --hp= argument: " + val + " is not a float!")
                exit_program()
            elif float(val) < 0.0 or float(val) > 1.0:
                print("error in --hp= argument: " + val + " must be between 0.0 and 1.0! (inclusive)")
                exit_program()
            hp = float(val)
            
        #hour command
        elif opt == 'hr':
            if not val.isdigit():
                print("error in --hr= argument: " + val + " is not an integer!")
                exit_program()
            elif int(val) not in range(24):
                print("error in --hr= argument: " + val + " must be between 0 and 23! (inclusive)")
                exit_program()
            hr = hr_boost[int(val)]
        
        #second hour ratio + ratio command
        elif opt == '--hr2':
            arr = val.split("%")
            if len(arr) != 2:
                print("error in --hr2= argument: format must be <num1>%<num2>!")
                exit_program()
            #hr2
            if not isdigit(arr[0]):
                print("error in --hr2= argument: " + arr[0] + " is not an integer!")
                exit_program()
            elif int(arr[0]) not in range(24):
                print("error in --hr2= argument: " + arr[0] + " must be between 0 and 23! (inclusive)")
                exit_program()
            hr2 = int(arr[0])
            #hr2_ratio
            if not arr[1].isfloat():
                print("error in --hr2= argument: " + arr[1] + " is not a float!")
                exit_program()
            elif (float(arr[1]) <= 0.0 or float(arr[1]) >= 1.0)  :
                print("error in --hp= argument: " + arr[1] + " must be between 0.0 and 1.0! (non-inclusive)")
                exit_program()
            hr2_ratio = int(arr[1])
            
    #number of occurrences
    if not got_n and len(args) > 0:
        if len(args) == 1:
            if not args[0].isdigit():
                print("error in number of occurences argument: " + args[0] + " is not an integer!")
                exit_program()
            elif int(args[0]) < 1:
                print("error in number of occurences argument: " + args[0] + " must be greater than 1")
                exit_program()
            else:
                n = int(args[0])
            
        else:
            print("error : too many arguments!")
            exit_program()
        
    hr = hr_boost[hr]
    hr2 = hr_boost[hr2]
        
    return n,stats,hp,hr,hr2,hr2_ratio
    
def handle_maybe_stats(stats, res):
    if res not in maybe_stats_res: return (res,)
    statsAdded = False
    
    match res:
        case 6:
            if stats[2] < 10+random.randint(1,5): 
                statsAdded = True
                stats[2] += 1
        case 7:
            if stats[1] < 10+random.randint(1,5): 
                statsAdded = True
                stats[1] += 1
        case 8:
            if stats[4] < 10+random.randint(1,10): 
                statsAdded = True
                stats[4] += 1
        case 9:
            if stats[3] < 10+random.randint(1,10): 
                statsAdded = True
                stats[3] += 1  
        case 12:
            if stats[2] < 30+random.randint(1,10): 
                statsAdded = True
                stats[2] += 1
        case 13:
            if stats[1] < 20+random.randint(1,10): 
                statsAdded = True
                stats[1] += 1            
        case 16:
            if stats[3] < 30+random.randint(1,20): 
                statsAdded = True
                stats[3] += 1
        case 19:
            if stats[4] < 40+random.randint(1,20): 
                statsAdded = True
                stats[4] += 1
        case 21:
            if stats[1] < 40+random.randint(1,10): 
                statsAdded = True
                stats[1] += 1
        case 23:
            if stats[2] < 40+random.randint(1,10): 
                statsAdded = True
                stats[2] += random.randint(1,3)
        case 32:
            if stats[1] < 90+random.randint(1,10): 
                statsAdded = True
                stats[1] += 1
    return (res, statsAdded)
                
    
    
def handle_stats(stats, res):
    res_t = handle_maybe_stats(stats, res)
    if(len(res_t) == 1): #no result found, not a maybe-stat
        match res:
            case 18:
                stats[0] += 1
            case 26:
                stats[0] += random.randint(1,2)
            case 30:
                stats[0] += random.randint(1,3)
            case 34:
                stats[2] += random.randint(1,3)
            case 38:
                stats[4] += random.randint(1,6)
            case 41:
                stats[3] += random.randint(1,6)
            case 45:
                stats[2] += random.randint(1,6)
            case 49:
                stats[1] += random.randint(1,2)
            case 53:
                stats[1] += random.randint(1,3) 
        return (res,)
    else:
        return res_t

    
    
#track_stats is an optimization that skips certain stat checks if they aren't needed
def main():
    n,start_stats,hp_ratio,hr,hr2,hr2_ratio = parse_args()  
    print("Performing coltzan's simulation for " + str(n) + " occurrences:")
    
    #rough estimation - 12 months in year, rounds down
    #2 visits a day = 2x
    est_15_days = math.floor((n/365)*12) * 2
    results = []
    update_interval = round(n/1000)
    stats = start_stats.copy()
    int_boost = get_int_boost(stats[0])
    
    print("Running daily simulation...")
    
    last_int = stats[0]
    
    for i in range(n):
        #progress bar
        if update_interval > 0:
            if i % update_interval == 0:
                perc = (i/n)*100
                print("Progress: %.1f%%" % (perc), end= '\r') 
                
        #15-day bonus is simulated clumped
        is_15_day = False
        if i < est_15_days: 
            is_15_day = True

        #hp boost bonus randomly determined by ratio
        hp_boost = math.isclose(hp_ratio, 1.0)
        if not hp_boost: #skips if check if ratio is 1.0
            if random.random() < hp_ratio:
                hp_boost = True
        
        #hr vs hr2 randomly determined by ratio
        hr_used = hr
        if(hr2_ratio != 0):
            if(random.random() < hr2_ratio):
                hr_used = hr2
        
        #recalculates int boost if relevant
        if int_boost < 6 and stats[0] != last_int: 
            int_boost = get_int_boost(stats[0])
            last_int = stats[0]
        
        #runs simulation and adds results
        res = handle_stats(stats, simulate_coltan(is_15_day, hp_boost, hr_used, int_boost))
        results.append(res)
        
        
    print("Daily simulation complete.\nSorting results...") 
    
    print_simulation_results(parse_results(results), n, est_15_days, start_stats, stats)

main()