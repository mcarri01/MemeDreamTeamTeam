import sys
import os
import threading
import Pyro4
# for networking
#import pyro

def main(argv):
	
	uri = raw_input("Enter uri: ").strip()
	board = Pyro4.Proxy(uri)
	b = board.readBoard()
	for i in b:
		print i
	
	
if __name__ == "__main__":
	main(sys.argv)
