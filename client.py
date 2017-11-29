import sys
import os
import threading
from fish import *
from title import *
import Pyro4
import socket
import time
import random
from datetime import datetime
import curses
from curses import wrapper
import signal

board = []
notDead = True

class DisplayThread(threading.Thread):

	def __init__(self, stdscr):
		threading.Thread.__init__(self)

		self.shutdown_flag = threading.Event()
		self.stdscr = stdscr
		self.titleText = ''.join(open("title.txt").readlines()).strip('\r')

	def run(self):
		lastTime = datetime.now()
		counter = 0
		while not self.shutdown_flag.is_set():
			currTime = datetime.now()
			delta = currTime - lastTime
			lastTime = currTime
			counter += delta.microseconds
			if counter >= 1000000/15:
				counter = 0
				global board
				b = board.readBoard()
				string = ''
				for line in b:
					for c in line:
						string += c
					string += '\n'
				self.stdscr.addstr(string, curses.color_pair(1))
				if not board.gameStarted():
					self.stdscr.addstr("Waiting for players...")
				self.stdscr.addstr(titleString)
				self.stdscr.move(0, 0)			
				board.clearBoard()

class FishThread(threading.Thread):

	def __init__(self, stdscr):
		threading.Thread.__init__(self)

		self.shutdown_flag = threading.Event()
		self.stdscr = stdscr

	def run(self):
		global board
		shutdown_flag = threading.Event()
		global notDead
		# maybe fix bounds
		initCol = random.randint(1, board.getWidth())
		initRow = random.randint(1, board.getHeight())
		fish = Fish("fish.txt", initRow, initCol, username)
		while not self.shutdown_flag.is_set():
			key = self.stdscr.getch()
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
			board.writeBoardFish(fish.getRow(), fish.getCol(), fish.getFish(), fish.getName())

class ServiceExit(Exception):
	pass

def receive_sig(signum, stack):
	raise ServiceExit


def initializeGame(waiting):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	IP = s.getsockname()[0]
	s.close()

	NS = Pyro4.locateNS(host=IP, port=9090, broadcast=True)

	uri = NS.lookup("example.board")
	global board
	board = Pyro4.Proxy(uri)
	board.addPlayer()
	if waiting != 'y':
		board.startGame()
	else:
		if board.numPlayers() > 1:
			board.startGame()


def main(stdscr, username, wait):
	initializeGame(wait)
	signal.signal(signal.SIGTERM, receive_sig)
	signal.signal(signal.SIGINT, receive_sig)
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
	stdscr.nodelay(True)

	dispThread = DisplayThread(stdscr)
	fishThread = FishThread(stdscr)
	try:
		dispThread.start()
		fishThread.start()
		while True:
			time.sleep(0.5)

	except ServiceExit:

		dispThread.shutdown_flag.set()
		fishThread.shutdown_flag.set()
		
		board.decrementPlayer()
		dispThread.join()
		fishThread.join()

if __name__ == "__main__":
	username = raw_input("Please choose your username: ")
	wait = raw_input("Wait for more players? (y/n): ")
	wrapper(main, username, wait)


