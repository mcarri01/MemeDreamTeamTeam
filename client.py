import sys
import os
import threading
from fish import *
from getch import *
import Pyro4
import socket
import time
import random

board = ''
notDead = True


def initializeGame():
	print(chr(27) + "[2J")
	print(chr(27) + "[H")

	# for now, we are simply using our own IP address, eventually
	# we will use a remote name server so we can just statically 
	# toss it in
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	IP = s.getsockname()[0]
	s.close()

	NS = Pyro4.locateNS(host=IP, port=9090, broadcast=True)

	uri = NS.lookup("example.board")

	global board
	board = Pyro4.Proxy(uri)

def retrieveDisplay():
	while True:
		print(chr(27) + "[2J")
		print(chr(27) + "[H")

		global board
		b = board.readBoard()
		for i in b:
			for j in i:
				sys.stdout.write(j)
			print ''
		time.sleep(1.0/100)

def controlFish():
	getch = Getch()
	initCol = random.randint(80, 129)
	initRow = random.randint(15, 20)
	fish = Fish("fish.txt", initRow, initCol)
	while notDead:
		key = 'b'
		#key = getch()
		currCol = fish.getCol()
		currRow = fish.getRow()
		if key == 'w':
			fish.setRow(currRow - 1)
		elif key == 'd':
			fish.setCol(currCol + 1)
		elif key == 's':
			fish.setRow(currRow + 1)
		elif key == 'a':
			fish.setCol(currCol - 1)
		# global board
		board.writeBoardFish(fish.getRow(), fish.getCol(), fish.getFish())
		board.clearBoard()

def main(args):
	initializeGame()
	displayThread = threading.Thread(target=retrieveDisplay, args=[])
	fishThread = threading.Thread(target=controlFish, args=[])

	displayThread.start()
	fishThread.start()

if __name__ == "__main__":
	main(sys.argv)
