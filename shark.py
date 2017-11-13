import os
import sys

class Shark(object):
    def __init__(self, filename, startcol, startrow):
        self.shark = []
        self.col = startcol
        self.row = startrow
        with open(filename) as f:
            for line in f:
                self.shark.append(line.split('\n')[0])

    def readShark(self):
        return self.shark

    def writeShark(self, board):
        tmpcol = self.col
        tmprow = self.row
        for line in self.shark:
            for char in line:
                board.writeBoard(char, tmpcol, tmprow)
                tmpcol += 1
            tmprow += 1


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

