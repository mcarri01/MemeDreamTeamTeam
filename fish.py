class Fish(object):
    def __init__(self, filename, startrow, startcol):
        self.fish = []
        self.col = startcol
        self.row = startrow
        with open(filename) as f:
            for line in f:
                tmp = line.split('\n')[0]
                tmp = list(tmp.encode("ascii"))
                self.fish.append(tmp)

    def getCol(self):
        return self.col

    def getRow(self):
        return self.row

    def getFish(self):
        return self.fish

    def setCol(self, col):
        self.col = col

    def setRow(self, row):
        self.row = row