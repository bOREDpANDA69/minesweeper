import sys
from termcolor import colored
'''

RULE 1:

    if tile's value minus number of flagged mines around it is equal to
    number of unflagged tiles:
        then every hidden tile is a mine

RULE 2:

    if number of flagged mines around tile is equal to tile's value:
        then every other unflagged tiles is safe

RULE 3:

    look for linked tiles and solve

    linked tiles are the tiles which are sure to have some mines in them
    but not known where

    x x here we can see that using above two rules this is impossible
    ? 3 we can see that the upper two '?' have 1 mine, using this to solve
    ? 2 the element 2 we can be sure that the lowest '?' is a mine. then
    ? 1 using 1 we can determine that the second ? is safe too.

RULE 4:

    if all unopened tiles == number of mines left
    all unopened tiles are mines.


'''

gamemap = """
? ? ? 0 ? ? ? 0 ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ? 0 0
? ? ? 0 ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? 0 0
0 0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? 0
? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 ? ? ? 0
? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? ? 0 0 0 ? ? ? 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? 0 0 0 0 ? ? ? 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 0 0 ? ? ? 0 0
0 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? 0 0 0 ? ? ? ? ? ? 0 0
0 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? ? ? ? ? ? ? ? 0 0
0 0 0 0 ? ? ? 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? ? ? ? 0 0 0 ? ?
0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ? 0 ? ? ? ? ?
0 ? ? ? 0 0 0 0 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ? 0 ? ? ? ? ?
0 ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? ? ? 0 0
0 ? ? ? ? ? ? ? ? ? 0 ? ? ? ? 0 0 ? ? ? ? 0 ? ? ? 0 0 0 0 0
? ? 0 ? ? ? ? ? ? ? 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 0 0
? ? 0 0 0 0 ? ? ? ? 0 ? ? ? ? 0 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0
? ? 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 0
0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 0
? ? ? ? 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? 0 ? ? ?
? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ? 0 ? ? ?
? ? ? ? ? ? ? 0 ? ? ? ? 0 ? ? ? ? ? 0 0 0 0 ? ? ? 0 0 ? ? ?
0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0
0 0 ? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
0 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? 0 0 0 0
0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
"""

result = """
1 x 1 0 1 1 1 0 1 x 2 x 1 0 0 0 1 x 1 0 0 0 0 0 0 1 1 1 0 0
1 1 1 0 1 x 2 2 3 2 2 1 1 0 0 0 1 1 2 1 1 0 0 0 0 1 x 1 0 0
0 0 0 1 2 2 2 x x 2 1 1 0 0 0 0 0 0 1 x 1 0 0 0 0 1 2 2 1 0
1 1 1 1 x 1 1 2 2 2 x 1 1 1 1 0 0 0 1 1 1 0 0 0 0 0 2 x 2 0
2 x 1 1 1 1 1 1 1 1 1 1 1 x 2 1 0 0 0 1 1 1 0 0 0 0 2 x 2 0
x 2 1 0 0 0 1 x 1 0 0 0 2 3 x 1 0 0 0 1 x 1 0 0 0 0 1 1 1 0
1 1 0 0 0 0 2 2 2 0 0 0 1 x 2 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0
0 0 0 0 0 0 1 x 1 0 0 0 2 2 2 0 1 1 1 0 0 0 1 1 1 1 x 1 0 0
0 0 0 0 1 1 2 1 1 0 0 0 1 x 1 0 1 x 1 1 1 2 2 x 1 1 1 1 0 0
0 0 0 0 1 x 1 0 0 0 0 0 1 1 1 0 2 2 2 2 x 3 x 2 1 0 0 0 1 1
0 0 0 0 1 1 1 0 0 0 0 1 1 1 0 0 1 x 1 2 x 4 2 2 0 1 1 1 1 x
0 1 1 1 0 0 0 0 0 0 0 1 x 1 0 0 1 2 2 2 1 2 x 1 0 1 x 1 1 1
0 1 x 2 1 2 1 1 0 0 0 1 1 1 0 0 0 1 x 1 0 1 2 2 1 1 1 1 0 0
0 1 1 2 x 2 x 3 2 1 0 1 2 2 1 0 0 1 2 2 1 0 1 x 1 0 0 0 0 0
1 1 0 1 1 2 2 x x 1 0 1 x x 1 0 0 0 1 x 1 0 1 2 2 1 0 0 0 0
x 1 0 0 0 0 2 3 3 1 0 1 2 2 1 0 0 0 1 1 1 0 0 2 x 2 0 0 0 0
1 1 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 0 0 0 0 0 0 2 x 3 1 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 1 x 1 0 0 0 1 1 1 0 1 2 x 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 2 x 2 0 1 2 2 1 0 0 0
1 2 2 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 x 2 0 1 x 1 0 1 1 1
1 x x 1 1 1 1 0 1 1 1 0 0 1 1 2 1 1 0 1 1 1 1 2 2 1 0 1 x 1
1 2 3 2 2 x 1 0 1 x 2 1 0 1 x 3 x 2 0 0 0 0 1 x 1 0 0 1 1 1
0 0 1 x 3 2 2 0 1 2 x 1 1 2 2 3 x 3 1 0 0 0 1 1 1 0 0 0 0 0
0 0 1 1 2 x 1 0 0 1 1 2 2 x 2 2 2 x 2 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 1 x 4 x 1 1 1 2 x 1 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 2 2 x 2 1 0 0 1 1 1 1 x 2 1 1 0 0 0 0
0 0 0 0 0 1 1 2 1 2 x 1 1 1 1 0 0 1 2 2 1 1 1 2 x 2 1 1 1 1
0 0 0 0 0 1 x 4 x 4 2 1 0 0 0 0 0 2 x x 2 2 2 2 3 x 2 1 x 1
0 0 0 0 0 1 2 x x x 1 0 0 0 0 0 0 2 x 3 2 x x 1 2 x 2 1 1 1
"""

mines = 87
map = [i.split() for i in gamemap.strip().split('\n')]
result = [i.split() for i in result.strip().split('\n')]
row, col = len(result[0]), len(result)
usableTiles = []

def printinfo():
    for i in range(col):
        for j in range(row):
            if (i, j) in usableTiles:
                print(colored(map[i][j], 'green'), end = ' ')
            else:
                print(map[i][j], end = ' ')
        print()
    
def open(i, j):
    if result[i][j] == 'x':
        printinfo()
        print(i, j)
        sys.exit("MINE!")
    return int(result[i][j])

def isInArray(x, y):
    for i in x:
        if i not in y:
            return False
    return True

def removeSubarray(x, y):
    for i in x:
        y.remove(i)
    return y

def issubset(sub, set):
    if len(sub) == len(set):
        return False
    for i in sub:
        if i not in set:
            return False
    return True

def getAdj(i, j):

    a = [(-1,-1), (-1, 0), (-1, 1),
         ( 0,-1), ( 0, 0), ( 0, 1),
         ( 1,-1), ( 1, 0), ( 1, 1)]
    
    out = []
    for x, y in a:
        if -1 < x+i < col and -1 < y+j < row:
            out.append((x+i, y+j))
    return out


def createUsableTiles():

    for i in range(col):
        for j in range(row):
            if map[i][j] == '0':
                for a,b in getAdj(i, j):
                    map[a][b] = open(a, b)
                    usableTiles.append((a, b))
    
    usableTiles[:] = list(set(usableTiles))

def filterUsableTiles():

    usableTiles[:] = [(i, j) for i, j in usableTiles if not (map[i][j] == countMinesAroundTile(i, j) and countUnopened(i, j) == 0)]

def countMinesAroundTile(a, b):

    mine = 0
    for i, j in getAdj(a, b):
        if map[i][j] == 'x':
            mine += 1
    return mine

def countUnopened(a, b):
    x = 0
    for i, j in getAdj(a, b):
        if map[i][j] == '?':
            x += 1
    return x

def rule1():
    print("INSIDE RULE 1")
    global mines
    flag = False
    for i, j in usableTiles:
        minearound = countMinesAroundTile(i, j)
        if minearound == map[i][j]:
            continue
        if countUnopened(i, j) == map[i][j]-minearound:
            for x, y in getAdj(i, j):
                if map[x][y] == '?':
                    map[x][y] = 'x'
                    mines -= 1
                    flag = True
    return flag
        
def rule2():
    print("INSIDE RULE 2")
    flag = False
    for i, j in usableTiles:
        if map[i][j]-countMinesAroundTile(i, j) == 0:
            for k, l in getAdj(i, j):
                if map[k][l] == '?':
                    flag = True
                    map[k][l] = open(k, l)
                    usableTiles.append((k, l))
    filterUsableTiles()
    return flag


def rule3():
    print("INSIDE RULE 3")
    global mines
    linkedTiles = []
    flag = False
    for i, j in usableTiles:
        mine, unopened = 0, 0
        unopenedIndex = []
        for k, l in getAdj(i, j):
            if map[k][l] == '?':
                unopened += 1
                unopenedIndex.append((k, l))
            elif map[k][l] == 'x':
                mine += 1
        
        if map[i][j] - mine - 1 == 0:
            linkedTiles.append(unopenedIndex)
    moreUsableTiles = []

    for i in linkedTiles:
        for j in linkedTiles:
            if issubset(i, j):
                linkedTiles.remove(j)

    for i, j in usableTiles:
        adj = getAdj(i, j)
        UNOPENED, mine, m = 0, 0, 0
        UNOPENEDINDEX = []
        for k, l in adj:
            if map[k][l] == '?':
                UNOPENED += 1
                UNOPENEDINDEX.append((k, l))
            elif map[k][l] == 'x':
                mine += 1

        for x in linkedTiles:
            if isInArray(x, UNOPENEDINDEX):
                UNOPENED -= len(x)            
                removeSubarray(x, UNOPENEDINDEX)
                m += 1

        if map[i][j]-mine-m == 0:
            for p, q in UNOPENEDINDEX:
                flag = True
                map[p][q] = open(p, q)
                moreUsableTiles.append((p, q))
        elif map[i][j]-mine-1 == UNOPENED:
            for p, q in UNOPENEDINDEX:
                flag = True
                map[p][q] = 'x'
                mines -= 1
    usableTiles.extend(moreUsableTiles)
    filterUsableTiles()
    return flag

def rule4():
    global mines
    flag = False
    unopened = 0
    unopenedIndex = []
    for i in range(col):
        for j in range(row):
            if map[i][j] == '?':
                unopened += 1
                unopenedIndex.append((i, j))
    if unopened == mines:
        for i, j in unopenedIndex:
            map[i][j] = 'x'
            flag = True
    return flag

def solve():
    
    createUsableTiles()
    filterUsableTiles()
    while mines > 0:
        x = rule1()
        printinfo()
        input()
        y = rule2()
        printinfo()
        input()
        if not (x or y):
            z = rule3()
            printinfo()
            input()
            if not z:
                if rule4():
                    print("breaking from rule4")
                    break
                print("Can't solve. mines left: ", mines)
                return '?'
    rule1()
    rule2()
    printinfo()
    return '\n'.join(' '.join(i) for i in map)
solve()