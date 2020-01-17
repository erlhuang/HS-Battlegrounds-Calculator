import requests
import json

data = {}

playerBoard = []
opponentBoard = []

#A doubly linked list connecting all minions on a board state 
#Lot to implement( Logic handling for deathrattles, figuring out how to implement order, etc)
#Deathrattle is tricky 
#Other effects: Windfury, poison 
class Minions():
    def __init__(self, name, attack, hp, golden, shield, poison, windfury):
        self.name = name 
        self.attack = attack
        self.hp = hp
        self.golden = golden 
        self.shield = shield 
        self.poison = poison 
        self.windfury = windfury 
    

tideHunter = Minions('Murloc Tidehunter',2,1, false, false, false, false )
playerBoard.append(tideHunter)

#Edge cases to account for:
# microbots on already existing Deathrattles 
#making sure there is room for deathrattles and we never overflow 
#how to calculate all possible permutations?
#for now, just have a simulation of the outcome of one possible battle?
with open('2cost.json') as json_file:
    jsonData = json.load(json_file)
    for p in jsonData:
        print(p['name'])
    print(jsonData)
