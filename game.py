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

def testRead():
	while not dinnerBell:

		print(chr(27) + "[2J")
		print(chr(27) + "[H")

		global board
		b = board.readBoard()
		for i in b:
			for j in i:
				sys.stdout.write(j)
			print ''
		time.sleep(1.0/100)

def swimShark(startRow, startCol):
	s = Shark("shark.txt", startRow, startCol)

	offScreen = board.writeBoardShark(s.row, s.col, s.vertMove, s.horizMove, 9, 55, s.shark)

	prevCol = 0
	prevRow = 0

	lastTime = datetime.now()
	counter = 0

	while not offScreen:
		# currTime = datetime.now()
		# delta = currTime - lastTime
		# lastTime = currTime

		# counter += delta.microseconds
		# if counter >= 1000000/24:
		# 	counter = 0
			
		if int(prevCol) == int(s.getCol()) and int(prevRow) == int(s.getRow()):
			prevCol = s.getCol()
			prevRow = s.getRow()
			s.move(board)
			continue

		offScreen = board.writeBoardShark(s.row, s.col, s.vertMove, s.horizMove, 9, 55, s.shark)

		board.clearBoard()
		
		prevCol = s.getCol()
		prevRow = s.getRow()
		
		s.move(board)

	global dinnerBell
	dinnerBell = True

def main(argv):
	print(chr(27) + "[2J")
	print(chr(27) + "[H")

	processesStart = []
	#IP = subprocess.check_output("ifconfig |grep inet\ ", shell=True).split(' ')[5]
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	IP = s.getsockname()[0]
	s.close()
	print IP
	processesStart.append(threading.Thread(target = startServer, args = [IP]))
	processesStart.append(threading.Thread(target = startBoard, args = [IP]))

	for p in processesStart:
		p.start()

	boardLock.acquire()
	boardLock.release()

	NS = Pyro4.locateNS(host=IP, port=9090, broadcast=True)

	uri = NS.lookup("example.board")

	global board
	board = Pyro4.Proxy(uri)

	# Doesn't need to be locked, because threads being created and started
	# will be sequentially afterwards
	# board.clearBoard()

	threads = []

	swimShark(-5, -60)
	threads.append(threading.Thread(target=swimShark, args=[-5, -60]))
	threads.append(threading.Thread(target=testRead))
	#threads.append(threading.Thread(target=swimShark, args=[0,0]))

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	for process in processes:
		os.killpg(os.getpgid(process.pid), signal.SIGTERM)


if __name__ == "__main__":
	main(sys.argv)
