from __future__ import print_function
import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Board(object):
    def __init__(self):
        self.board = []
        self.height = 30
        self.width = 130
        for j in range(self.height):
            string = ['+']
            for i in range(self.width-1):
                if j != 0 and j != (self.height - 1):
                    string.append(' ')
                else:
                    string.append('-')
            string.append('+')
            self.board.append(string)

    def clearBoard(self):
        for i in range(1, self.height - 1):
            for j in range(1, self.width):
                self.board[i][j] = ' '

    def readBoard(self):
        return self.board

    def writeBoard(self, c, row, col):
        self.board[row][col] = c

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

#        self.board[row][col] = c



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
            host = '10.0.0.185')

if __name__=="__main__":
    main()
