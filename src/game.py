import sys
import os
import threading
import Pyro4
from shark import *
import time
from datetime import datetime
import subprocess
import multiprocessing as mp
import signal
import socket
import random
import signal
import requests

#serverLock = threading.Semaphore(0)
boardLock = threading.Semaphore(0)
processes = []
board = ''
running = True

def startBoard(IP):

	processes.append(subprocess.Popen("python -m Pyro4.naming -n %s > /dev/null" % IP, shell=True, preexec_fn=os.setsid))
	time.sleep(3)
	processes.append(subprocess.Popen("python board.py %s > /dev/null" % IP, shell=True, preexec_fn=os.setsid))
	time.sleep(3)
	boardLock.release()

def swimShark(startRow, startCol):
	s = Shark("models/shark.txt", startRow, startCol)

	offScreen = board.writeBoardShark(s.row, s.col, s.vertMove, s.horizMove, 9, 55, s.shark)

	prevCol = 0
	prevRow = 0

	lastTime = datetime.now()
	counter = 0

	while not offScreen and running:
		currTime = datetime.now()
		delta = currTime - lastTime
		lastTime = currTime

		counter += delta.microseconds
		if counter >= 1000000/20:
			counter = 0
			board.clearBoard()
			offScreen = board.writeBoardShark(s.row, s.col, s.vertMove, s.horizMove, 9, 55, s.shark)

			prevCol = s.getCol()
			prevRow = s.getRow()
			
			s.move(board)

def endserver(signum, stack):
	global running
	running = False

def main(argv):
	signal.signal(signal.SIGINT, endserver)
	processesStart = []
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	IP = s.getsockname()[0]
	s.close()
	processesStart.append(threading.Thread(target = startBoard, args = [IP]))

	for p in processesStart:
		p.start()

	boardLock.acquire()
	boardLock.release()

	NS = Pyro4.locateNS(host=IP, port=9090, broadcast=True)
	time.sleep(5)
	uri = NS.lookup("example.board")

	global board
	board = Pyro4.Proxy(uri)

	threads = []
	print ("Running server on " + IP + "...let the games begin!")
	prevPlayers = board.numPlayers()
	while running:
		currPlayers = board.numPlayers()
		if currPlayers > prevPlayers:
			print ("Player joined the game!")
			prevPlayers = currPlayers
		elif currPlayers < prevPlayers:
			print ("Player has died!")
			prevPlayers = currPlayers
		if board.gameStarted():
			wave = board.getWave()
			for i in range (0, wave):
				randomY = random.randint(-10, board.getHeight())
				for i in range(0, wave):
					thread = threading.Thread(target=swimShark, args=[randomY, -70])
					threads.append(thread)
				for thread in threads:
					thread.start()
				for thread in threads:
					thread.join()
				threads = []
			board.updateWave()

	for thread in threads:
		thread.join()

	board.endGame()
	for process in processes:
		os.killpg(os.getpgid(process.pid), signal.SIGTERM)


if __name__ == "__main__":
	main(sys.argv)
