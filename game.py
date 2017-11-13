import sys
import os
import threading
import Pyro4
from shark import *
# for networking
#import pyro

def main(argv):
#	board = Pyro4.Proxy("PYRONAME:example.board@10.0.0.230:8080")
	NS = Pyro4.locateNS(host="10.0.0.185", port=9090, broadcast=True)
	#uri = "PYRO:Pyro.NameServer@10.0.0.230:9090"
	uri = NS.lookup("example.board")
	board = Pyro4.Proxy(uri)
	# print NS
	# board = NS.lookup("example.board@10.0.0.230")
	b = board.readBoard()
	for i in b:
		print i

	s = Shark("shark.txt", 100, 5)

	shark = s.readShark()

	s.writeShark(board)

	for i in b:
		print i


	
	
if __name__ == "__main__":
	main(sys.argv)
