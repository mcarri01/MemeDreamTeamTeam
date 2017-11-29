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

serverLock = threading.Semaphore(0)
boardLock = threading.Semaphore(0)
processes = []
dinnerBell = False
board = ''

def startBoard(IP):
	serverLock.acquire()
	processes.append(subprocess.Popen("python board.py %s > /dev/null" % IP, shell=True, preexec_fn=os.setsid))
	boardLock.release()

def startServer(IP):
	processes.append(subprocess.Popen("python -m Pyro4.naming -n %s > /dev/null" % IP, shell=True, preexec_fn=os.setsid))
	serverLock.release()

def swimShark(startRow, startCol):
	s = Shark("shark.txt", startRow, startCol)

	offScreen = board.writeBoardShark(s.row, s.col, s.vertMove, s.horizMove, 9, 55, s.shark)

	prevCol = 0
	prevRow = 0

	lastTime = datetime.now()
	counter = 0

	while not offScreen:
		currTime = datetime.now()
		delta = currTime - lastTime
		lastTime = currTime

		counter += delta.microseconds
		if counter >= 1000000/24:
			counter = 0

			offScreen = board.writeBoardShark(s.row, s.col, s.vertMove, s.horizMove, 9, 55, s.shark)

			prevCol = s.getCol()
			prevRow = s.getRow()
			
			s.move(board)

	global dinnerBell
	dinnerBell = True

def main(argv):
	print(chr(27) + "[2J")
	print(chr(27) + "[H")

	processesStart = []
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	IP = s.getsockname()[0]
	s.close()
	processesStart.append(threading.Thread(target = startServer, args = [IP]))
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

	while True:
		randomY = random.randint(1, board.getHeight())
		thread = threading.Thread(target=swimShark, args=[randomY, 1])
		thread.start()
		time.sleep(5)

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	for process in processes:
		os.killpg(os.getpgid(process.pid), signal.SIGTERM)


if __name__ == "__main__":
	main(sys.argv)
