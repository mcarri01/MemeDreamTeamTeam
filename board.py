from __future__ import print_function
import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Board(object):
    def __init__(self):
        self.board = ""
        for j in range(height):
            string = '+'
            for i in range(width):
                if j != 0 and j != (height - 1):
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