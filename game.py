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
	NS = Pyro4.locateNS(host="10.245.164.240", port=9090, broadcast=True)

	uri = NS.lookup("example.board")

	board = Pyro4.Proxy(uri)

	b = board.clearBoard()

	b = board.readBoard()

	s = Shark("shark.txt", -5, -60)

	s.writeShark(board)

	b = board.readBoard()

	while True:		
		for i in b:
			for j in i:
				sys.stdout.write(j)
			print ''

		b = board.clearBoard()
		s.move(board)
		s.writeShark(board)
		b = board.readBoard()

		os.system('cls' if os.name == 'nt' else 'clear')

	
	
if __name__ == "__main__":
	main(sys.argv)
