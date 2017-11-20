import os
import sys

class Shark(object):
    def __init__(self, filename, startrow, startcol):
        self.shark = []
        self.col = startcol
        self.row = startrow
        self.vertMove = .25
        self.horizMove = .25
        with open(filename) as f:
            for line in f:
                tmp = line.split('\n')[0]
                tmp = list(tmp.encode("ascii"))
                self.shark.append(tmp)

    def readShark(self):
        return self.shark

    #def writeShark(self, board):
        

    def move(self, board):
        self.col += self.horizMove
        self.row += self.vertMove

        self.row %= (board.getHeight() - 1)


    def getCol(self):
        return self.col

    def getRow(self):
        return self.row



