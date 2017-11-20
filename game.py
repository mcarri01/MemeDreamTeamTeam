import sys
import os
import threading
import Pyro4
from shark import *
import time
from datetime import datetime
# for networking
#import pyro

def main(argv):
	os.system('cls' if os.name == 'nt' else 'clear')
	NS = Pyro4.locateNS(host="10.0.0.185", port=9090, broadcast=True)

	uri = NS.lookup("example.board")

	board = Pyro4.Proxy(uri)

	board.clearBoard()

	s = Shark("shark.txt", -5, -60)
	board.writeBoard(s.row, s.col, s.vertMove, s.horizMove, 9, 55, s.shark)

	b = board.readBoard()

	prevCol = 0
	prevRow = 0

	lastTime = datetime.now()
	counter = 0

	while True:
		currTime = datetime.now()
		delta = currTime - lastTime
		lastTime = currTime

		counter += delta.microseconds
		if counter >= 1000000/24:
		# os.system('cls' if os.name == 'nt' else 'clear')
			counter = 0
			
			if int(prevCol) == int(s.getCol()) and int(prevRow) == int(s.getRow()):
				prevCol = s.getCol()
				prevRow = s.getRow()
				s.move(board)
				continue

			print(chr(27) + "[2J")
			print(chr(27) + "[H")

			for i in b:
				for j in i:
					sys.stdout.write(j)
				print ''

			board.clearBoard()
			
			prevCol = s.getCol()
			prevRow = s.getRow()

			#seconds = 1.0/40
			#time.sleep(seconds)
			
			s.move(board)

			board.writeBoard(s.row, s.col, s.vertMove, s.horizMove, 9, 55, s.shark)
			b = board.readBoard()


	
	
if __name__ == "__main__":
	main(sys.argv)
