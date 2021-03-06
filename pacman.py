from random import *
from sets import Set

class Layout:
    
    def __init__(self,width,height,ncoins,nwalls,numGhosts):
        self.width = width
        self.height = height
        self.ncoins = ncoins
        self.nwalls = nwalls
        self.coinPos = Set()
        self.wallPos = Set()
        self.ghostPositions = []
        self.numGhosts = numGhosts
        self.pacman = Pacman()
        self.ghosts = [ Ghost() for i in range(self.numGhosts) ]

    def makeInitialLayout(self):
        self.grid = [['.' for i in range(self.width)] for j in range(self.height)]
        #Wall position
        while len(self.wallPos) < self.nwalls:
            temp = 0
            if not temp:
                row = randint(0,self.height-1)
                for i in range(self.width-1):
                    if random() < 0.8:
                        wally = randint(0,self.width-1)
                        self.grid[row][wally] = 'X'
                        self.wallPos.add((row,wally))
                        if len(self.wallPos)+1 > self.nwalls:
                            break
                temp = True                    
            else:
                column = randint(0,self.width-1)
                for i in range(self.height -1):
                    if random() < 0.8:
                        wallx = randint(0,self.height-1)
                        self.grid[wallx][column] = 'X'
                        self.wallPos.add((wallx,column))
                        if len(self.wallPos)+1 > self.nwalls:
                            break
                temp = False
       
        #Coin position
        while len(self.coinPos) < self.ncoins :
            coinx,coiny = randint(0,self.height-1),randint(0,self.width-1)
            if self.grid[coinx][coiny] == '.':
                self.grid[coinx][coiny] = 'C'
                self.coinPos.add((coinx,coiny))
            
        #Pacman position
        self.pacman.position = randint(0,self.height-1),randint(0,self.width-1)
        while not self.grid[self.pacman.position[0]][self.pacman.position[1]] == '.':
            self.pacman.position = randint(0,self.height-1),randint(0,self.width-1)
        self.grid[self.pacman.position[0]][self.pacman.position[1]] = 'P'
        
        #Ghost position
        i = 0
        while len(self.ghostPositions) < self.numGhosts :
            ghostx,ghosty = randint(0,self.height-1),randint(0,self.width-1)
            if self.grid[ghostx][ghosty] == '.':
                self.grid[ghostx][ghosty] = 'G'
                self.ghostPositions.append((ghostx,ghosty))
                self.ghosts[i].position = (ghostx,ghosty)
                i += 1

class Game(Layout):

    def __init__(self,width,height,ncoins,nwalls,numGhosts):
        self.eatenCoins = []
        Layout.__init__(self,width,height,ncoins,nwalls,numGhosts)
        self.isWin = False
        self.isLose = False
    def getScore(self):
        self.score = len(self.eatenCoins)
        
        return self.score

    def printState(self):
        print "\n"
        for row in self.grid:
            print "  ".join(map(str,row))

    def getMove(self):
        print "Score: ",self.getScore()
        self.move = str(raw_input("Next move:"))

    def playGame(self):
        while not self.isLose or not self.isWin:
            self.checkEnd()
            if self.isWin or self.isLose:
                break
            self.getMove()
            self.makeMove(self.move)
            self.printState()


    def makeMove(self,move):
        self.pacman.moveLegal(move,self)
        for i in range(self.numGhosts):
           self.ghosts[i].moveLegal(self)

            
    def checkEnd(self):
        for i in range(self.numGhosts):
            if self.pacman.position == self.ghosts[i].position:
                self.isLose = True
                print 'You lose! :('
                return
        print 'eaten coins:',self.eatenCoins
        print 'ncoins : ',self.ncoins
        if len(self.eatenCoins) == self.ncoins :
                self.isWin = True
                print 'You win! :D '
                return
class Person:

    def __init__(self, index=0):
        self.index = index


class Pacman(Person):
    def __init__(self):
        self.position = (0,0)
    def moveLegal(self,move,gameState):
        legal = False
        if move == 'a':
            nextx,nexty = self.position[0],self.position[1]-1
            if nexty >= 0 and gameState.grid[nextx][nexty]!='X':
                 legal = True
        if move == 'd':
            nextx,nexty = self.position[0],self.position[1]+1
            if nexty < gameState.width and gameState.grid[nextx][nexty]!='X':
                legal = True

        elif move == 'w':
            nextx,nexty = self.position[0]-1,self.position[1]
            if nextx >= 0 and gameState.grid[nextx][nexty]!='X':
                legal = True
        elif move == 's':
            nextx,nexty = self.position[0]+1,self.position[1]
            if nextx < gameState.height and gameState.grid[nextx][nexty]!='X':
                legal = True
        if legal:
            if gameState.grid[nextx][nexty] == 'C':
                gameState.eatenCoins.append((nextx,nexty))
                gameState.grid[nextx][nexty] = '.'
            gameState.grid[nextx][nexty] = 'P'
            gameState.grid[self.position[0]][self.position[1]] = '.'
            self.position = (nextx,nexty)

        
class Ghost(Person):
    def __init__(self):
        self.position = (0, 0)
    def moveLegal(self,gameState):
        legal = False
        while not legal:
            r = random()
            if r < 0.25:
                nextx,nexty = self.position[0],self.position[1]-1
                if nexty >= 0 and gameState.grid[nextx][nexty]!='X' and gameState.grid[nextx][nexty]!='C':
                    assigned = True
            elif r < 0.5 :
                nextx,nexty = self.position[0],self.position[1]+1
                if nexty < gameState.width and gameState.grid[nextx][nexty]!='X' and gameState.grid[nextx][nexty]!='C':
                    legal = True

            elif r < 0.75:
                nextx,nexty = self.position[0]-1,self.position[1]
                if nextx >= 0 and gameState.grid[nextx][nexty]!='X' and gameState.grid[nextx][nexty]!='C':
                    legal = True
            else:
                nextx,nexty = self.position[0]+1,self.position[1]
                if nextx < gameState.height and gameState.grid[nextx][nexty]!='X' and gameState.grid[nextx][nexty]!='C':
                    legal = True
            if legal:
                gameState.grid[nextx][nexty] = 'G'
                gameState.grid[self.position[0]][self.position[1]] = '.'
                self.position = (nextx,nexty)


if __name__ == '__main__':
    game = Game(15,20,20,20,4)

    game.makeInitialLayout()
    game.printState()
    game.playGame()
