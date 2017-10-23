import sys
import os
import threading
# for networking
#import pyro

board = []
fish = []
shark = []

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
	drawBoard(30, 200)
	readShark("shark.txt")
	readFishy("fish.txt")
	for i in shark:
		print i
	for i in fish:
		print i
	for i in board:
		print i
	
	
if __name__ == "__main__":
	main(sys.argv)
