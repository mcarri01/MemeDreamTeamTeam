import sys
import os
import threading
import Pyro4
from shark import *
import time
# for networking
#import pyro

def main(argv):
	os.system('cls' if os.name == 'nt' else 'clear')
	NS = Pyro4.locateNS(host="192.168.0.71", port=9090, broadcast=True)

	uri = NS.lookup("example.board")

	board = Pyro4.Proxy(uri)

	board.clearBoard()

	#b = board.readBoard()

	s = Shark("shark.txt", -5, -60)

	s.writeShark(board)

	b = board.readBoard()
	k = 0

	prevCol = 0
	prevRow = 0

	while True:
		if int(prevCol) == int(s.getCol()) and int(prevRow) == int(s.getRow()):
			prevCol = s.getCol()
                	prevRow = s.getRow()
			
			s.move(board)
			k+=1
			print k
			continue
		for i in b:
			for j in i:
				sys.stdout.write(j)
			print ''

		board.clearBoard()
		
		prevCol = s.getCol()
		prevRow = s.getRow()
		
		s.move(board)
		

		s.writeShark(board)
		b = board.readBoard()
		k += 1
		print k
		#os.system('cls' if os.name == 'nt' else 'clear')

	
	
if __name__ == "__main__":
	main(sys.argv)
