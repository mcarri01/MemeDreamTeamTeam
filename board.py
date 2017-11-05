from __future__ import print_function
import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Board(object):
    def __init__(self):
        self.board = []
	height = 20
	width = 30
        for j in range(20):
            string = '+'
            for i in range(30):
                if j != 0 and j != (20 - 1):
                    string += ' '
                else:
                    string += '-'
            string += '+'
            self.board.append(string)

    def readBoard(self):
        return self.board

    def writeBoard(self, newBoard):
        self.board = newBoard

def main():
    Pyro4.Daemon.serveSimple(
            {
                Board: "example.board"
            },
            ns = False)

if __name__=="__main__":
    main()
