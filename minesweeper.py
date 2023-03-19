import os
import selenium
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from termcolor import colored

d = {
    'easy' : (9,9),
    'medium' : (16, 16),
    'hard' : (16, 30),
    'evil' : (20, 30)
}
dmin = {
    'easy' : 10,
    'medium' : 40,
    'hard' : 99,
    'evil' : 130
}
difficulty = input("Choose difficulty: Easy Medium Hard Evil\n").lower()
col, row = d[difficulty]
mines = dmin[difficulty]
map = [['?']*row for i in range(col)]
usableTiles = []

print("Starting in ", end= '')
for i in range(3, 0, -1):
    print(i, end = '')
    sleep(0.1)
    print('.',end = '')
    sleep(0.1)
    print('.', end = '')
    sleep(0.1)
    print('.', end = '')

os.environ['PATH'] += r"D:/projects/minesweeper"
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://minesweeper.online/new-game/ng")
driver.implicitly_wait(3)

if difficulty != 'easy':
    id = 'level_select_1'
    lvl = {'medium' : '2', 'hard' : '3', 'evil' : '4'}
    id += lvl[difficulty]
    cell = driver.find_element(By.ID, id)
    cell.click()


def printinfo():
    for i in range(col):
        for j in range(row):
            if (i, j) in usableTiles:
                print(colored(map[i][j], 'green'), end = ' ')
            else:
                print(map[i][j], end = ' ')
        print()

def getstarted():
    for i in range(col):
        for j in range(row):
            cell = driver.find_element(By.ID, f'cell_{j}_{i}')
            if cell.get_attribute('class') == 'cell size24 hd_closed start':
                map[i][j] = 0
                usableTiles.append((i, j))
                cell.click()
                break
    updateMap()

def updateMap():
    for i in range(col):
        for j in range(row):
            if map[i][j] == 'x':
                continue
            cell = driver.find_element(By.ID, f'cell_{j}_{i}')
            cellClass = cell.get_attribute('class').split()
            if cellClass[2] == 'hd_opened':
                map[i][j] = int(cellClass[3][-1])
                usableTiles.append((i, j))
    filterUsableTiles()
            

def open(i, j):
    cell = driver.find_element(By.ID, f'cell_{j}_{i}')
    cell.click()
    cell = driver.find_element(By.ID, f'cell_{j}_{i}')
    updateMap()
    cellValue = cell.get_attribute('class').split()
    return int(cellValue[-1][-1])

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

def getUnopened():
    count = 0
    out = []
    for i in range(col):
        for j in range(row):
            if map[i][j] == '?':
                count += 1
                out.append((i, j))
    return [count, out]


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
    unopened, unopenedIndex = getUnopened()
    if unopened == mines:
        for i, j in unopenedIndex:
            map[i][j] = 'x'
            flag = True
    return flag

def rule5():
    print("INSIDE RULE 5")

    def printdecoy():
        for i in range(col):
            for j in range(row):
                if (i, j) in usableTiles:
                    print(colored(decoy[i][j], 'red'), end = ' ')
                else:
                    print(decoy[i][j], end = ' ')
            print()

    def countminesaround(i, j):
        out = 0
        for i, j in getAdj(i, j):
            if decoy[i][j] == 'x':
                out += 1
        return out

    def countunopened(i, j):
        out = 0
        for i, j in getAdj(i, j):
            if decoy[i][j] == '?':
                out += 1
        return out
    def countallunopened():
        out = 0
        for i in range(col):
            for j in range(row):
                if decoy[i][j] == '?':
                    out += 1
        return out

    def rule51(MINE):
        print("INSIDE RULE 5.1")
        flag = [False, False]
        for i, j in usableTiles:
            minearound = countminesaround(i, j)
            if minearound == decoy[i][j]:
                continue
            if minearound > decoy[i][j]:
                flag[1] = True
                return flag
            if countunopened(i, j) == decoy[i][j]-minearound:
                for x, y in getAdj(i, j):
                    if decoy[x][y] == '?':
                        decoy[x][y] = 'x'
                        flag[0] = True
                        MINE[0] -= 1
                        if MINE[0] == 0:
                            if countallunopened() > 0:
                                flag[1] = True
                                return flag
                        if MINE[0] < 0:
                            flag[1] = True
                            return flag
        if MINE[0] == 0:
            if countallunopened() > 0:
                flag[1] = True
                return flag
        if MINE[0] < 0:
            flag[1] = True
            return flag
        if countallunopened() == 0 and MINE[0] > 0:
            flag[1] = True
            return flag
        return flag
    
    def rule52():
        print("INSIDE RULE 5.2")
        for i, j in usableTiles:
            if decoy[i][j]-countminesaround(i, j) == 0:
                for k, l in getAdj(i, j):
                    if decoy[k][l] == '?':
                        decoy[k][l] = 'n'
    
    def rule53(MINE):
        print("INSIDE RULE 5.3")
        flag = [False, False]
        linkedTiles = []
        for i, j in usableTiles:
            mine, unopened = 0, 0
            unopenedIndex = []
            for k, l in getAdj(i, j):
                if decoy[k][l] == '?':
                    unopened += 1
                    unopenedIndex.append((k, l))
                elif decoy[k][l] == 'x':
                    mine += 1
            
            if decoy[i][j] - mine - 1 == 0:
                linkedTiles.append(unopenedIndex)

        for i in linkedTiles:
            for j in linkedTiles:
                if issubset(i, j):
                    linkedTiles.remove(j)

        for i, j in usableTiles:
            adj = getAdj(i, j)
            UNOPENED, mine, m = 0, 0, 0
            UNOPENEDINDEX = []
            for k, l in adj:
                if decoy[k][l] == '?':
                    UNOPENED += 1
                    UNOPENEDINDEX.append((k, l))
                elif decoy[k][l] == 'x':
                    mine += 1

            for x in linkedTiles:
                if isInArray(x, UNOPENEDINDEX):
                    UNOPENED -= len(x)            
                    removeSubarray(x, UNOPENEDINDEX)
                    m += 1

            if decoy[i][j]-mine-m == 0:
                for p, q in UNOPENEDINDEX:
                    decoy[p][q] = 'n'
                    flag[0] = True
                    
            elif decoy[i][j]-mine-1 == UNOPENED:
                for p, q in UNOPENEDINDEX:
                    decoy[p][q] = 'x'
                    flag[0] = True
                    MINE[0] -= 1
                    if MINE[0] < 0:
                        flag[1] = True
                        return flag
        return flag

    def rule54(MINE):
        return MINE[0] == countallunopened()

    global mines
    unopened, unopenedIndex = getUnopened()
    for i, j in unopenedIndex:
        decoy = [i[:] for i in map]
        decoy[i][j] = 'x'
        MINE = [mines-1]
        while True:

            x, y = rule51(MINE)
            printdecoy()
            a, b = rule53(MINE)
            printdecoy()
            if (y or b):
                print("MINES LEFT:", MINE)
                p, q = rule51(MINE)
                printdecoy()
                input()
                l, m = rule53(MINE)
                printdecoy()
                if (q or m) and rule54(MINE):
                    return (i, j)
            if not (x or a):
                break
            rule52()
    
    return False

        



def solve():
    getstarted()
    createUsableTiles()
    filterUsableTiles()
    while mines > 0:
        x = rule1()
        printinfo()
        y = rule2()
        printinfo()
        if not (x or y):
            z = rule3()
            printinfo()
            if not z:
                if rule4():
                    print("breaking from rule4")
                    break
                w = rule5()
                if w == False:
                    print("Cant solve. mines left: ", mines)
                    return '?'
                else:
                    i, j = w
                    usableTiles.append(w)
                    map[i][j] = open(i, j)

    rule1()
    rule2()
    printinfo()
    print("Solved!")
solve()
while True:
    pass