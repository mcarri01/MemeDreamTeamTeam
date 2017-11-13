import os
import sys

class Shark(object):
    def __init__(self, filename, startrow, startcol):
        self.shark = []
        self.col = startcol
        self.row = startrow
        with open(filename) as f:
            for line in f:
                tmp = line.split('\n')[0]
                tmp = list(tmp.encode("ascii"))
                self.shark.append(tmp)

    def readShark(self):
        return self.shark

    def writeShark(self, board):
        tmprow = self.row
        for line in self.shark:
            tmpcol = self.col
            for char in line:
                # if tmprow >= (board.getHeight() - 1):
                #     tmprow = 1
                if tmpcol > (board.getWidth() - 1):
                    tmpcol += 1
                    continue
                elif tmpcol < 0:
                    tmpcol += 1
                    continue

                if tmpcol == 0:
                    tmpcol += 1

                board.writeBoard(char, tmprow, tmpcol)
                
                tmpcol += 1

            tmprow += 1
            if tmprow == 0:
                tmprow += 1

    def move(self, board):
        self.col += 0
        self.row += 1

        # if self.row < 1:
        #     self.row = board.getHeight() - 2;
        # elif self.row >= (board.getHeight() - 1):
        #     self.row = 1



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

