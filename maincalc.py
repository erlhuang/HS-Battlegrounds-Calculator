# import requests
import json
import random 
#Two drops for shredder... 
twoDrops = {}
#Account for Baron, Mama Bear, Ornery Direhorn, etc...
specialBehaviors = {}
deathRattles = {}

#This is a dictionary of bools that keeps track of whether there's a Cobalt, if there's a 
#Mama bear, total murlocs on board, etc. 
playerTurn = True
specialsOnBoard = {}
#A doubly linked list connecting all minions on a board state 
#Lot to implement( Logic handling for deathrattles, figuring out how to implement order, etc)
#Deathrattle is tricky 
#Other effects: Windfury, poison 
#Need to keep track of tribes too? For warleader interactions, mech summons 
#for cobalt, mech deaths for junkbot, and 
class Minions():
    def __init__(self, name, attack, hp, golden, shield, poison, windfury):
        self.name = name 
        self.attack = attack
        self.hp = hp
        self.golden = golden 
        self.shield = shield 
        self.poison = poison 
        self.windfury = windfury 
        self.left = None 
        self.right = None 

class playerVar():
    def __init__(self):
        self.nextAttack = 0
        self.taunts = None
        self.board = None
        self.player = None

def printMinion(minion):
    print(minion.name + " " + str(minion.attack) + " " \
        + str(minion.hp) + " (", end="")
    if minion.golden:
        print("G", end=" ")
    if minion.shield:
        print("DS", end=" ")
    if minion.poison:
        print("P", end=" ")
    if minion.windfury:
        print("W", end=" ")
    print(")", end=" ")

#Attacker minion initiates attack with receiving minion 
def minionFight(attacker, receiving): #attacker, receiving are playerVars 
    attackingMin = attacker.board[attacker.nextAttack]
    randNum = random.randrange(0,len(receiving.board))
    receivingMin = receiving.board[randNum]
    print(attackingMin.name + " " + str(attackingMin.attack) + "/" + str(attackingMin.hp) +  " battling " \
         + receivingMin.name + " " + str(receivingMin.attack) + "/" + str(receivingMin.hp))
    if attackingMin.shield:
        if receivingMin.attack > 0:
            attackingMin.shield = False
    else:
        if receivingMin.poison:
            attackingMin.hp = 0
        else:
            attackingMin.hp = attackingMin.hp - receivingMin.attack 
    #logic to deal damage to opponent minion
    if receivingMin.shield:
        receivingMin.shield = False
    else:
        if attackingMin.poison:
            receivingMin.hp = 0
        else:
            receivingMin.hp = receivingMin.hp - attackingMin.attack
    attacker.board[attacker.nextAttack] = attackingMin 
    receiving.board[randNum] = receivingMin
    handleMinionDeaths(attackingMin, receivingMin, attacker, receiving)
    #Do some logic to trigger deathrattles and other specific behaviors later... 

    
def handleMinionDeaths(playerMin, oppMin, playerBoard, opponentBoard): # --> nextAttack, nextAttack2
    #this also needs to handle next attack logic for deaths ]
    playerIndex = playerBoard.board.index(playerMin)
    if playerMin.hp <= 0:
        if(playerBoard.player):
            print("Player's ", end=" ")
        else:
            print("Opponent's ", end=" ")
        print(playerMin.name + " died." )
        playerBoard.board.remove(playerMin)
    else:
        playerBoard.nextAttack = playerIndex + 1 % len(playerBoard.board)
    if oppMin.hp <= 0:
        if(opponentBoard.player):
            print("Player's ", end=" ")
        else:
            print("Opponent's ", end=" ")
        print(oppMin.name + " died.")
        opponentIndex = opponentBoard.board.index(oppMin)
        opponentBoard.board.remove(oppMin)
        if opponentIndex != opponentBoard.nextAttack:
            if len(opponentBoard.board) == 0:
                return
            opponentBoard.nextAttack = opponentBoard.nextAttack + 1 % (len(opponentBoard.board))
    else:
        if len(opponentBoard.board) == 0:
            return
        # opponentBoard.nextAttack = opponentBoard.nextAttack + 1 % (len(opponentBoard.board))   

    
def simulateFight(playerBoard, opponentBoard):
    #Player turn true means it's players turn to attack, false means it's opponents turn
    #These variables keep track of next minions in line to attack
    playerClass = playerVar()
    oppClass = playerVar() 
    playerClass.board = playerBoard 
    playerClass.player = True
    oppClass.board = opponentBoard
    oppClass.player = False
    if len(playerClass.board) == len(oppClass.board):
        if(random.randrange(1) == 0):
            playerTurn = True 
        else:
            playerTurn = False
    elif len(playerBoard) > len(opponentBoard):
        playerTurn = True
    else:
        playerTurn = False 
    while len(playerClass.board) > 0 and len(oppClass.board) > 0:
        print("Board state for player: ")
        for minion in playerClass.board:
            printMinion(minion)
        print()
        print("Board state for opponent: ")
        for minion in oppClass.board:
            printMinion(minion)
        print()
        if playerTurn == True:
            print("Player's turn: ")
            #Must account for taunt! Have a dic of enemy taunts too?
            minionFight(playerClass, oppClass)
        else: #Means it's opponents turn to fight..
            print("Opponent's turn: ") 
            minionFight(oppClass, playerClass)
        #switch turns!
        playerTurn = not playerTurn 
    if len(playerClass.board) > 0:
        print("Player won!")
    elif len(oppClass.board) > 0:
        print("Opponent won!")
    else:
        print("It's a tie!")

def main():
    tideHunter = Minions('Murloc Tidehunter',2,1,False,False,False,False)
    tideHunter2 = Minions('Murloc Tidehunter',2,1,False,False,False,False)
    alleyCat = Minions('Alley Cat',1,1,False,False,False,False)
    alleyCat2 = Minions('Alley Cat',1,1,False,True,True,False)
    wrathw = Minions('Wrath Weaver', 10, 10, False, False, False, False)
    playerBoard = []
    opponentBoard = []
    playerBoard.append(tideHunter)
    playerBoard.append(alleyCat)
    opponentBoard.append(alleyCat2)
    opponentBoard.append(tideHunter2)
    playerBoard.append(wrathw)
    #Edge cases to account for:
    # microbots on already existing Deathrattles 
    #making sure there is room for deathrattles and we never overflow 
    #how to calculate all possible permutations?
    #for now, just have a simulation of the outcome of one possible battle?
    with open('2cost.json') as json_file:
        jsonData = json.load(json_file)
        for p in jsonData:
            twoDrops[p['name']] = p
    
    simulateFight(playerBoard, opponentBoard)

if __name__ == "__main__":
    main()

