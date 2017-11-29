from __future__ import print_function
import Pyro4
import sys

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Board(object):
    def __init__(self):
        self.board = []
        self.started = False
        self.playerCount = 0
        self.height = 30
        self.width = 100
        for j in range(self.height):
            string = ['+']
            for i in range(self.width-1):
                if j != 0 and j != (self.height - 1):
                    string.append(' ')
                else:
                    string.append('-')
            string.append('+')
            self.board.append(string)

    def clearBoard(self):
        for i in range(1, self.height - 1):
            for j in range(1, self.width):
                self.board[i][j] = ' '
        
    def readBoard(self):
        return self.board
        
    def writeBoardShark(self, row, col, vertMove, horizMove, height, width, shark):
        if col > self.width + 1:    
            return self.board, True
        if row == 0:
            if vertMove < 0:
                row = self.height - 2
            else:
                row += 1
        if row < 0:
            row %= (self.height - 1)

        tmprow = int(row)

        for line in shark:

            if tmprow == 0:
                tmprow += 1
                continue
            elif tmprow < 1:
                tmprow += 1
                continue
            if tmprow >= self.height - 1:
                tmprow = 1

            tmpcol = int(col)

            for c in line:
                if tmpcol > (self.width - 1):
                    tmpcol += 1
                    continue
                elif tmpcol < 0:
                    tmpcol += 1
                    continue

                if tmpcol == 0:
                    tmpcol += 1
                if c != ' ':
                    self.board[tmprow][tmpcol] = c
                tmpcol += 1
            tmprow += 1
        
        return False

    def writeBoardFish(self, row, col, fish, name):
        tmpcol = int(col)
        tmprow = int(row)
        for c in name:
            self.board[tmprow][tmpcol] = c
            tmpcol += 1

        tmprow = int(row) + 1
        for line in fish:
            tmpcol = int(col)
            for c in line:
                self.board[tmprow][tmpcol] = c
                tmpcol += 1
            tmprow += 1
        
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def numPlayers(self):
        return self.playerCount

    def addPlayer(self):
        self.playerCount += 1

    def decrementPlayer(self):
        self.playerCount -= 1

    def startGame(self):
        self.started = True

    def endGame(self):
        self.started = False

    def gameStarted(self):
        return self.started

def main(args):
    Pyro4.config.SERVERTYPE = "multiplex"
    Pyro4.Daemon.serveSimple(
            {
                Board: "example.board"
            },
            ns = True,
            host = args[1])

if __name__=="__main__":
    main(sys.argv)
