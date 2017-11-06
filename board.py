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


# def readShark(filename):
#  +        with open(filename) as f:
#  +                for line in f:
#  +                        shark.append(line.split('\n')[0])
          
#  +def readFishy(filename):
#  +  with open(filename) as f:
#  +      for line in f:
#  +          fish.append(line.split('\n')[0])
#  +  
#  +def drawBoard(height, width):
#  +  for j in range(height):
#  +      string = '+'
#  +      for i in range(width):
#  +          if j != 0 and j != (height - 1):
#  +              string += ' '
#  +          else:
#  +              string += '-'
#  +      string += '+'
#  +      board.append(string



def main():
    Pyro4.Daemon.serveSimple(
            {
                Board: "example.board"
            },
            ns = True,
            host = '10.0.0.230')

if __name__=="__main__":
    main()
