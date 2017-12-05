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
import re
import argparse

board = []
dead = False

class DisplayThread(threading.Thread):

	def __init__(self, stdscr):
		threading.Thread.__init__(self)

		self.shutdown_flag = threading.Event()
		self.stdscr = stdscr
		self.titleText = ''.join(open("models/title.txt").readlines()).strip('\r')

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
				wave = board.getWave()
				string = ''
				for line in b:
					for c in line:
						string += c
					string += '\n'
				self.stdscr.addstr(string, curses.color_pair(1))
				if not board.gameStarted():
					self.stdscr.addstr("Waiting for players...\n")
				else:
					s = "Current wave: " + str(wave) + "\n"
					self.stdscr.addstr(s, curses.A_BOLD)
				self.stdscr.addstr(titleString)
				self.stdscr.move(0, 0)			
				board.clearBoard()

class FishThread(threading.Thread):

	def __init__(self, stdscr, username):
		threading.Thread.__init__(self)

		self.shutdown_flag = threading.Event()
		self.username = username
		self.stdscr = stdscr
		self.username = username

	def run(self):
		global board
		global dead
		shutdown_flag = threading.Event()
		# maybe fix bounds
		initCol = random.randint(1, board.getWidth())
		initRow = random.randint(1, board.getHeight())
		fish = Fish("models/fish.txt", initRow, initCol, self.username)
		while not self.shutdown_flag.is_set():
			if not dead:
				key = self.stdscr.getch()
				curses.flushinp
				currCol = fish.getCol()
				currRow = fish.getRow()
				if key == ord('w') and currRow != 1:
					fish.setRow(currRow - 1)
				elif key == ord('d') and currCol != board.getWidth()-fish.getFishWidth():
					diff = (board.getWidth())-currCol-1
					if fish.getDisplayNameLen() > diff:
						fish.setDisplayName(fish.getDisplayName()[:diff])
					fish.setCol(currCol + 1)
				elif key == ord('s') and currRow != board.getHeight()-fish.getFishHeight()-2:
					fish.setRow(currRow + 1)
				elif key == ord('a') and currCol != 1:
					if fish.getDisplayNameLen() < fish.getNameLen():
						fish.oneMoreChar()
					fish.setCol(currCol - 1)
				collision = board.writeBoardFish(fish.getRow(), fish.getCol(), fish.getFish(), fish.getDisplayName())
				if collision:
					dead = True

class ServiceExit(Exception):
	pass

def receive_sig(signum, stack):
	raise ServiceExit


def initializeGame(waiting, ip):
	# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# s.connect(("8.8.8.8", 80))
	# IP = s.getsockname()[0]
	# s.close()

	NS = Pyro4.locateNS(host=ip, port=9090, broadcast=True)

	uri = NS.lookup("example.board")
	global board
	board = Pyro4.Proxy(uri)
	board.addPlayer()
	if waiting != 'y':
		board.startGame()
	else:
		if board.numPlayers() > 1:
			board.startGame()


def parseArgs(argv):

    parser = argparse.ArgumentParser(description='Client program for SharksAndMinnows game!')
    parser.add_argument('-i', dest='ip', type=str,
                        help='IPv4 Address of Name Server')

    return parser.parse_args().ip


def main(stdscr, username, wait, ip):
	initializeGame(wait, ip)
	signal.signal(signal.SIGTERM, receive_sig)
	signal.signal(signal.SIGINT, receive_sig)
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
	stdscr.nodelay(True)

	dispThread = DisplayThread(stdscr)
	fishThread = FishThread(stdscr, username)
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
	ip = parseArgs(sys.argv)
	username = raw_input("Please choose your username: ")
	username = re.sub(r'[^a-zA-Z]', '', username)
	wait = raw_input("Wait for more players? (y/n): ")
	wrapper(main, username, wait, ip)


