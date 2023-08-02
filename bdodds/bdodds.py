# Battledome Loot Simulator by Metamagic
# Trans rights are human rights ^^
# metty says hi

import random
import re

TWO_ROLL_RATIO = 1.0 # % of time two arena prizes are rolled
CHALLENGER_ROLL_RATIO = 1,0 # % of time challenger prizes are rolled

# ===============
# list population
# ===============

arenaFighters =  {
    "Central Arena":(
        "Boochi",
        "Chia Clown",
        "Down For Maintenance Pteri",
        "Eyrieki",
        "Flaming Meerca",
        "Kasuki Lu",
        "Kauvara",
        "Lab Ray Scientist",
        "Mootix Warrior",
        "Mr. Chuckles",
        "Punchbag Bob",
        "Shadow Usul",
        "Tax Beast",
        "Turmaculus"
    ),
    "Dome of the Deep":(
        "Chiazilla",
        "Giant Spectral Mutant Walein",
        "Koi Warrior",
        "Slug Monster",
        "The Drenched"
    ),
    "Frost Arena":(
        "Donny",
        "Lady Frostbite",
        "Snow Beast",
        "Snow Faerie",
        "The Snowager",
        "Valin"
    ),
    "Neocola Centre":(
        "Commander Garoo",
        "Evil Sloth Clone",
        "Mutated Chia",
        "Neopets V2",
        "Robo Grarrl",
        "S750 Kreludan Defender Bot",
        "Space Faerie"
    ),
    "Pango Palladium":(
        "Advisor Broo",
        "Ghost Lupe",
        "Lava Ghoul",
        "Meerca Henchmen",
        "Ryshu the Nimmo",
        "Tekkitu the Witch Doctor",
        "Tiki Tack Man"
    ),
    "Rattling Cauldron":(
        "Balthazar",
        "Count Von Roo",
        "Edna",
        "Giant Ghostkerchief",
        "Greedie Kadoatie",
        "Jelly Chia",
        "Meuka",
        "Mummy",
        "Pant Devil",
        "Qasalan Mummy",
        "Sidney",
        "Spider Grundo",
        "The Black Pteri",
        "The Brain Tree",
        "The Esophagor",
        "Vira",
        "Zafara Rogue"
    ),
    "Ugga Dome":(
        "Cave Chia",
        "Cybunny Scout",
        "Giant Hungry Malevolent Chomby",
        "Grarrg",
        "Harry the Mutant Moehog",
        "Highland Chia",
        "Kastraliss",
        "Magnus the Torch",
        "Quiggle Warlord",
        "Sabre-X"
    ),
    "Cosmic Dome":(
        "Giant Space Fungus",
        "Jetsam Ace"
    )
}

class Arena:
    def __init__ (self,a):
        self.name=a
        self.loot=[]

class Challenger:
    def __init__ (self,a,b):
        self.name=a
        self.arena=getArena(a)
        self.difficulty=b
        self.loot=[]

def getArena(name):
    #find arena name
    arenaName = ""
    i = 0
    for fl in list(arenaFighters.values()):
        if fl.count(name) > 0: 
            arenaName = list(arenaFighters.keys())[i]
            break
        i += 1
    #find arena
    for a in arenaList:
        if a.name == arenaName: return a
    

def populateArenaList():
    arenaList = []
    file = open("arenaloot.txt", "r")
    
    line = file.readline()
    currArena = None
    
    #reads each line of NT dump
    while line != '':
        line = line.strip()
        if len(line) > 3: #weird chars
            #create new object
            if "%" not in line:
                if currArena != None: arenaList.append(currArena)
                currArena = Arena(line)
            #add to loot table
            else:
                res = re.search(r"(.*) - (.*) %", line)
                currArena.loot.append((res.group(1), float(res.group(2))))
        line = file.readline()
    
    if currArena != None: arenaList.append(currArena)
    return arenaList

def populateChallengerList():
    fighterList = []
    file = open("challengerloot.txt", "r")
    
    currFighter = None
    line = file.readline()
    
    #reads each line of NT dump
    while line != '':
        line = line.strip()
        if len(line) > 3:
            #create new object
            if "%" not in line:
                if currFighter != None: fighterList.append(currFighter)
                res = re.search(r"(.*) (\d)", line)
                if validFighter(res.group(1)): currFighter = Challenger(res.group(1), int(res.group(2)))
                else: currFighter = None
            #add to loot table
            else:
                res = re.search(r"(.*) - (.*) %", line)
                if currFighter != None: currFighter.loot.append((res.group(1), float(res.group(2))))
                
        line = file.readline()
    
    if currFighter != None: fighterList.append(currFighter)
    return fighterList

def validFighter(name):
    for namelist in list(arenaFighters.values()):
        if name in namelist: return True
    return False
    
#==================
# simulation stuffs
#==================

def getTotalWeight(list):
    sum = 0
    for (a, b) in list: sum += b
    return sum

#def getLoot(challenger):
    #shuffle loot
    #sort loot
    #key=x[1]

def main():        
    print("Finding Battledome odds for all challengers...")
    global arenaList 
    arenaList = populateArenaList()
    global fighterList
    fighterList = sorted(populateChallengerList(), key = lambda f: (f.name, f.difficulty))
    
main()