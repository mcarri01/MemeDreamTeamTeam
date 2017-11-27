import sys

row = 15
col = 70
board = []
for j in range(30):
    string = ['+']
    for i in range(130-1):
        if j != 0 and j != (30 - 1):
            string.append(' ')
        else:
            string.append('-')
    string.append('+')
    board.append(string)

fish = []
with open("fish.txt") as f:
    for line in f:
        tmp = line.split('\n')[0]
        tmp = list(tmp.encode("ascii"))
        fish.append(tmp)

tmprow = int(row)
for line in fish:
    tmpcol = int(col)
    for c in line:
        board[tmprow][tmpcol] = c
        tmpcol += 1
    tmprow += 1


for i in board:
    for j in i:
        sys.stdout.write(j)
    print ''