# import requests
import json
import random 
#Two drops for shredder... 
twoDrops = {}
#Account for Baron, Mama Bear, Ornery Direhorn, etc...
specialBehaviors = {}
deathRattles = {
}

#This is a dictionary of bools that keeps track of whether there's a Cobalt, if there's a 
#Mama bear, total murlocs on board, etc. 
playerTurn = True
specialsOnBoard = {}

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

plyrClass = playerVar()
oppClass = playerVar()

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
    handleMinionDeaths(attackingMin, receivingMin, attacker, receiving)
    #Do some logic to trigger deathrattles and other specific behaviors later... 

    
def handleMinionDeaths(attkMinion, rcvMin, attkClass, rcvClass): # --> nextAttack, nextAttack2
    #this also needs to handle next attack logic for deaths ]
    playerIndex = attkClass.board.index(attkMinion)
    if attkMinion.hp <= 0:
        if(attkClass.player):
            print("Player's ", end=" ")
        else:
            print("Opponent's ", end=" ")
        print(attkMinion.name + " died." )
        attkClass.board.remove(attkMinion)
    else:
        attkClass.nextAttack = playerIndex + 1 % len(attkClass.board)
    if rcvMin.hp <= 0:
        if(rcvClass.player):
            print("Player's ", end=" ")
        else:
            print("Opponent's ", end=" ")
        print(rcvMin.name + " died.")
        opponentIndex = rcvClass.board.index(rcvMin)
        rcvClass.board.remove(rcvMin)
        if opponentIndex != rcvClass.nextAttack:
            if len(oppClass.board) == 0:
                return
            rcvClass.nextAttack = rcvClass.nextAttack + 1 % (len(rcvClass.board))
    else:
        if len(rcvClass.board) == 0:
            return
        # oppClass.nextAttack = oppClass.nextAttack + 1 % (len(oppClass.board))   

    
def simulateFight(plyrBoard, oppBoard):
    #Player turn true means it's players turn to attack, false means it's opponents turn
    #These variables keep track of next minions in line to attack
    # attkClass = playerVar()
    # oppClass = playerVar() 
    plyrClass.board = plyrBoard 
    plyrClass.player = True
    oppClass.board = oppBoard
    oppClass.player = False
    if len(plyrClass.board) == len(oppClass.board):
        if(random.randrange(1) == 0):
            playerTurn = True 
        else:
            playerTurn = False
    elif len(plyrClass.board) > len(oppClass.board):
        playerTurn = True
    else:
        playerTurn = False 
    while len(plyrClass.board) > 0 and len(oppClass.board) > 0:
        print("Board state for player: ")
        for minion in plyrClass.board:
            printMinion(minion)
        print()
        print("Board state for opponent: ")
        for minion in oppClass.board:
            printMinion(minion)
        print()
        if playerTurn == True:
            print("Player's turn: ")
            #Must account for taunt! Have a dic of enemy taunts too?
            minionFight(plyrClass, oppClass)
        else: #Means it's opponents turn to fight..
            print("Opponent's turn: ") 
            minionFight(oppClass, plyrClass)
        #switch turns!
        playerTurn = not playerTurn 
    if len(plyrClass.board) > 0:
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
    plyrClass = []
    oppBoard = []
    plyrClass.append(tideHunter)
    plyrClass.append(alleyCat)
    oppBoard.append(alleyCat2)
    oppBoard.append(tideHunter2)
    plyrClass.append(wrathw)
    #Edge cases to account for:
    # microbots on already existing Deathrattles 
    #making sure there is room for deathrattles and we never overflow 
    #how to calculate all possible permutations?
    #for now, just have a simulation of the outcome of one possible battle?
    with open('2cost.json') as json_file:
        jsonData = json.load(json_file)
        for p in jsonData:
            twoDrops[p['name']] = p
    
    simulateFight(plyrClass, oppBoard)

if __name__ == "__main__":
    main()

