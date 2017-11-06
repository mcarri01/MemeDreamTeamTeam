import sys
import os  
import threading
 # for networking
 #import pyro
board = []
shark = []
fish = []


def readShark(filename):
     with open(filename) as f:
             for line in f:
                     shark.append(line.split('\n')[0])
		  
def readFishy(filename):
	with open(filename) as f:
		for line in f:
			fish.append(line.split('\n')[0])
	
def drawBoard(height, width):
	for j in range(height):
		string = '+'
		for i in range(width):
			if j != 0 and j != (height - 1):
				string += ' '
			else:
				string += '-'
		string += '+'
		board.append(string)
		  
def main(argv):
	drawBoard(50, 400)
	readShark("shark.txt")
	readFishy("fish.txt")
	startcol = 1
	row = 200
	print type(board[0][0])
	for j in shark:
		col = startcol
		for i in j:
			print type(i)
			board[col][row] = i
			col+=1
		row+=1
	for i in fish:
		print i
	for i in board:
		print i
	
	
if __name__ == "__main__":	
	main(sys.argv) 