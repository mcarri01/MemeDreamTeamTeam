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
from functools import reduce

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


class SharkManager(threading.Thread):
    def __init__(self, numSharks):
        threading.Thread.__init__(self)

        self.numSharks = numSharks
        self.sharks = []
        for i in range(self.numSharks):
            if i == 0:
                self.sharks.append(Shark("models/shark.txt", 13, -55))
            else:
                self.sharks.append(Shark("models/shark.txt", 1, -55))

    def run(self):
        sharksInfo = []
        for s in self.sharks:
            sharksInfo.append({'row': s.row, 'col': s.col, 'vertMove': s.vertMove, 'horizMove': s.horizMove, 'shark': s.shark})
        status = board.writeBoardShark(sharksInfo)
        lastTime = datetime.now()
        counter = 0
        offScreen = reduce((lambda x, y: x and y), status, True)
        while not offScreen and running:
            currTime = datetime.now()
            delta = currTime - lastTime
            lastTime = currTime

            counter += delta.microseconds
            if counter >= 1000000/30:
                counter = 0
                board.clearBoard()
                sharksInfo = []
                for s in self.sharks:
                    sharksInfo.append({'row': s.row, 'col': s.col, 'vertMove': s.vertMove, 'horizMove': s.horizMove, 'shark': s.shark})
                status = board.writeBoardShark(sharksInfo)
                offScreen = reduce((lambda x, y: x and y), status, True)

                for shark in self.sharks:
                    shark.move(board)


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

    print ("Running server on " + IP + "...let the games begin!")
    prevPlayers = board.numPlayers()
    global running
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
            sharkManager = SharkManager(wave)
            sharkManager.start()
            sharkManager.join()
            board.updateWave()

    board.endGame()
    for process in processes:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)


if __name__ == "__main__":
    main(sys.argv)
