import sys
import os
import threading
from fish import *
from getch import *
import Pyro4
import socket
import time
import random
from datetime import datetime
import curses
from curses import wrapper
import signal

board = ''
notDead = True

def initializeGame():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	IP = s.getsockname()[0]
	s.close()

	NS = Pyro4.locateNS(host=IP, port=9090, broadcast=True)

	uri = NS.lookup("example.board")
	global board
	board = Pyro4.Proxy(uri)

def retrieveDisplay(stdscr):
	lastTime = datetime.now()
	counter = 0
	while True:
		currTime = datetime.now()
		delta = currTime - lastTime
		lastTime = currTime
		counter += delta.microseconds
		if counter >= 1000000/10:
			counter = 0
			global board
			b = board.readBoard()
			string = ''
			for line in b:
				for c in line:
					string += c
				string += '\n'
			stdscr.addstr(string)
			stdscr.move(0, 0)			
			board.clearBoard()

def controlFish(stdscr):
	# maybe fix bounds
	initCol = random.randint(1, board.getWidth())
	initRow = random.randint(1, board.getHeight())
	fish = Fish("fish.txt", initRow, initCol)
	while notDead:
		key = stdscr.getch()
		curses.flushinp
		currCol = fish.getCol()
		currRow = fish.getRow()
		if key == ord('w'):
			fish.setRow(currRow - 1)
		elif key == ord('d'):
			fish.setCol(currCol + 1)
		elif key == ord('s'):
			fish.setRow(currRow + 1)
		elif key == ord('a'):
			fish.setCol(currCol - 1)

		board.writeBoardFish(fish.getRow(), fish.getCol(), fish.getFish())

def main(stdscr, args):
	initializeGame()

	stdscr.nodelay(True)
	stdscr.clear()

	displayThread = threading.Thread(target=retrieveDisplay, args=[stdscr])
	fishThread = threading.Thread(target=controlFish, args=[stdscr])
	displayThread.setDaemon(True)
	fishThread.setDaemon(True)

	displayThread.start()
	fishThread.start()

	displayThread.join()
	fishThread.join()

if __name__ == "__main__":
	wrapper(main, sys.argv)
