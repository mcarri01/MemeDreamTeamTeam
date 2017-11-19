import os
import sys

class Shark(object):
    def __init__(self, filename, startrow, startcol):
        self.shark = []
        self.col = startcol
        self.row = startrow
        self.vertMove = .25
        self.horizMove = .5
        with open(filename) as f:
            for line in f:
                tmp = line.split('\n')[0]
                tmp = list(tmp.encode("ascii"))
                self.shark.append(tmp)

    def readShark(self):
        return self.shark

    def writeShark(self, board):
        if self.row == 0:
            if self.vertMove < 0:
                self.row = board.getHeight() - 2
            else:
                self.row += 1

        if self.row < 0:
            self.row %= (board.getHeight() - 1)

        tmprow = int(self.row)

        for line in self.shark:

            if tmprow == 0:
                tmprow += 1
                continue
            elif tmprow < 1:
                tmprow += 1
                continue
            if tmprow >= board.getHeight() - 1:
                tmprow = 1

            tmpcol = int(self.col)

            for char in line:
                if tmpcol > (board.getWidth() - 1):
                    tmpcol += 1
                    continue
                elif tmpcol < 0:
                    tmpcol += 1
                    continue

                if tmpcol == 0:
                    tmpcol += 1
		if char != ' ':
                	board.writeBoard(char, tmprow, tmpcol)
                tmpcol += 1
            tmprow += 1

    def move(self, board):
        self.col += self.horizMove
        self.row += self.vertMove

        # self.col %= (board.getWidth() - 1)
        self.row %= (board.getHeight() - 1)

        # if self.row < 1:
        #     self.row = board.getHeight() - 2;
        # elif self.row >= (board.getHeight() - 1):
        #     self.row = 1

    def getCol(self):
	return self.col

    def getRow(self):
        return self.row

# def readShark(filename):
#  +        with open(filename) as f:
#  +                for line in f:
#  +                        shark.append(line.split('\n')[0])
          
#  +def readFishy(filename):
#  +  with open(filename) as f:
#  +      for line in f:
#  +          fish.append(line.split('\n')[0])
#  +  
#  +def drawBoard(height, width):
#  +  for j in range(height):
#  +      string = '+'
#  +      for i in range(width):
#  +          if j != 0 and j != (height - 1):
#  +              string += ' '
#  +          else:
#  +              string += '-'
#  +      string += '+'
#  +      board.append(string

