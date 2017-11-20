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

serverLock = threading.Semaphore(0)
boardLock = threading.Semaphore(0)
processes = []

def startBoard(IP):
	serverLock.acquire()
	processes.append(subprocess.Popen("python board.py %s > /dev/null" % IP, shell=True, preexec_fn=os.setsid))
	boardLock.release()

def startServer(IP):
	processes.append(subprocess.Popen("pyro4-ns -n %s > /dev/null" % IP, shell=True, preexec_fn=os.setsid))
	serverLock.release()

def main(argv):
	print(chr(27) + "[2J")
	print(chr(27) + "[H")

	threads = []
	IP = subprocess.check_output("ifconfig |grep inet\ ", shell=True).split(' ')[5]
	threads.append(threading.Thread(target = startServer, args = [IP]))
	threads.append(threading.Thread(target = startBoard, args = [IP]))

	for thread in threads:
		thread.start()

	boardLock.acquire()

	NS = Pyro4.locateNS(host=IP, port=9090, broadcast=True)

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

	offScreen = False

	while not offScreen:
		currTime = datetime.now()
		delta = currTime - lastTime
		lastTime = currTime

		counter += delta.microseconds
		if counter >= 1000000/24:
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
			
			s.move(board)

			offScreen = board.writeBoard(s.row, s.col, s.vertMove, s.horizMove, 9, 55, s.shark)
			b = board.readBoard()

	for process in processes:
		os.killpg(os.getpgid(process.pid), signal.SIGTERM)

	
	
if __name__ == "__main__":
	main(sys.argv)
