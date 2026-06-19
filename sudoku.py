import math

debug = []
for x in range(32):
    debug += [False]

# use temporary debug grid (not user-input)
debug[0] = True
# use NYT 2026-06-15 medium (=False) or hard (=True) puzzle
debug[1] = True
# even harder puzzle in debug[1] (debug[2] == True: use the harder puzzle)
debug[2] = True
# test with an already-contradictory puzzle (debug[3] = unsolvable)
debug[3] = False


# puzzle entry line-by-line input from the user
# re-prompts line if there is a length error
# //// should add check for invalid characters in addition to only checking for line length
# returns False if deDimensionalize() fails
def initialPuzzleEntry():
    if debug[0] == False:
        premiseArray = []
        while len(premiseArray) < 9:
            entry = str(input("enter puzzle row " + str(len(premiseArray) + 1) + ": "))
            if len(entry) == 9:
                premiseArray += [entry]
            else: 
                print("ERROR: invalid entry")
        premise = deDimensionalize(premiseArray)
    if debug[0] == True:
        if debug[3] == False:
            if debug[1] == False:
                # NYT medium difficulty
                premise = [
                    "1","6"," "," "," "," "," "," "," ",
                    " ","2"," "," "," "," ","8","5"," ",
                    " ","5"," "," "," ","7","9"," ","1",
                    "2"," ","7"," "," "," "," "," ","8",
                    " "," "," "," ","4"," ","5"," "," ",
                    " ","3"," "," "," ","2"," "," "," ",
                    "9","4"," "," "," "," ","3"," "," ",
                    " "," "," "," ","5","1"," "," "," ",
                    "3"," "," ","6"," "," "," ","7"," "
                    ]
            if debug[1] == True:
                if debug[2] == False:
                    # NYT hard difficulty
                    premise = [
                        " "," ","2"," ","6"," "," "," "," ",
                        " "," ","6","8","1"," ","2"," "," ",
                        "8"," "," ","9"," "," "," ","7"," ",
                        " "," "," ","3"," "," "," "," "," ",
                        "1"," "," "," ","8"," "," ","2","9",
                        " "," "," ","2","5"," ","6"," "," ",
                        " "," ","7"," "," "," "," "," "," ",
                        "2"," ","4"," "," "," ","1","6","5",
                        " "," ","3"," "," "," "," ","8","7"
                        ]
                if debug[2] == True:
                    # super hard puzzle
                    premise = [
                        " "," "," ","1"," ","2"," "," "," ",
                        " ","6"," "," "," "," "," ","7"," ",
                        " "," ","8"," "," "," ","9"," "," ",
                        "4"," "," "," "," "," "," "," ","3",
                        " ","5"," "," "," ","7"," "," "," ",
                        "2"," "," "," ","8"," "," "," ","1",
                        " "," ","9"," "," "," ","8"," ","5",
                        " ","7"," "," "," "," "," ","6"," ",
                        " "," "," ","3"," ","4"," "," "," ",
                        ]
        else:
            premise = [
                " "," "," ","1"," ","1"," "," "," ", # was 000102000
                " ","6"," "," "," "," "," ","7"," ",
                " "," ","8"," "," "," ","9"," "," ",
                "4"," "," "," "," "," "," "," ","3",
                " ","5"," "," "," ","7"," "," "," ",
                "2"," "," "," ","8"," "," "," ","1",
                " "," ","9"," "," "," ","8"," ","5",
                " ","7"," "," "," "," "," ","6"," ",
                " "," "," ","3"," ","4"," "," "," ",
                ]
        print("debug[0] == True: len(premise) = " + str(len(premise)))
    return premise

def deDimensionalize(array):
    puzzle = []
    for x in array:
        print(x)
        for y in x:
            print(y)
            puzzle += [y]
    if len(puzzle) == 81:
        return puzzle
    else:
        print("ERROR: invalid puzzle length")
        return False

def initialize():
    premise = initialPuzzleEntry()
    if premise != False:
        pass
    else:
        return False

# collect initial puzzle entry from user
# retries if the puzzle entry is invalid
premise = False
while premise == False:
    premise = initialPuzzleEntry()

print("original premise")
print(premise[:9])
print(premise[9:18])
print(premise[18:27])
print(premise[27:36])
print(premise[36:45])
print(premise[45:54])
print(premise[54:63])
print(premise[63:72])
print(premise[72:])



def rowReduce(uGrid, index, value):
    uGridNew = uGrid
    iStart = 9*int(index/9)
    for x in range(9):
        if (iStart + x) != index:
            uGridNew[iStart + x] = uGridNew[iStart + x].replace(value, "")
        else:
            uGridNew[iStart + x] = value
    return uGridNew

def colReduce(uGrid, index, value):
    uGridNew = uGrid
    iStart = index
    for x in range(9):
        if (iStart + 9*x)%81 != index:
            uGridNew[(iStart + 9*x)%81] = uGridNew[(iStart + 9*x)%81].replace(value, "")
        else:
            uGridNew[(iStart + 9*x)%81] = value
    return uGridNew

def tbtReduce(uGrid, index, value):
    uGridNew = uGrid
    iStart = 27*int(index/27) + 3*int((index%9)/3) # gives top-left index of indexed 3x3 square
    for x in range(3):
        for y in range(3):
            if (iStart + x + 9*y) != index:
                uGridNew[(iStart + x + 9*y)] = uGridNew[(iStart + x + 9*y)].replace(value, "")
            else:
                uGridNew[(iStart + x + 9*y)] = value
    return uGridNew

def lookForSingleUs(uGrid):
    premise = []
    # checks for uGrid cells with a single potential solution
    for x in uGrid:
        if len(x) == 1:
            premise += [x]
        else:
            premise += [" "]
    # also check rows, columns, and 3x3s for potentials that only show up once
    xuGrid = uGrid
    # ROW
    for index in range(81):
        iStart = 9*int(index/9)
        for v in xuGrid[index]:
            if len(xuGrid[index]) > 1:
                # check rest of row to see if that v (value) shows up anywhere else
                tally = 0
                for c in range(9):
                    if xuGrid[iStart + c].find(v) != -1:
                        tally += 1
                if tally == 1:
                    xuGrid[index] = v
            else:
                continue
    # COL
    for index in range(81):
        iStart = index
        for v in xuGrid[index]:
            if len(xuGrid[index]) > 1:
                # check rest of column to see if that v (value) shows up anywhere else
                tally = 0
                for c in range(9):
                    if xuGrid[(iStart + 9*c)%81].find(v) != -1:
                        tally += 1
                if tally == 1:
                    xuGrid[index] = v
    # TBT
    for index in range(81):
        iStart = 27*int(index/27) + 3*int((index%9)/3)
        for v in xuGrid[index]:
            if len(xuGrid[index]) > 1:
                # check rest of 3x3 to see if that v (value) shows up anywhere else
                tally = 0
                for cX in range(3):
                    for cY in range(3):
                        if xuGrid[iStart + cX + 9*cY].find(v) != -1:
                            tally += 1
                if tally == 1:
                    xuGrid[index] = v
    return premise, xuGrid

def checkUTotal(uGrid):
    uTotal = 0
    for cell in uGrid:
        uTotal += len(cell)
    return uTotal

def initializeUGrid(premise):
    uGrid = []
    xPremise = premise
    for x in range(81):
        uGrid += ["123456789"]
    uTotal0 = 10*81 # initialize uTotal (total potential values in grid)
    uTotal1 = checkUTotal(uGrid)
    while uTotal0 > uTotal1:
        iter = 0
        print("iteration " + str(iter) + ": uTotal = " + str(uTotal0))
        uTotal0 = uTotal1
        for i in range(len(xPremise)):
            if xPremise[i] != " ":
                uGrid = rowReduce(uGrid, i, xPremise[i])
                uGrid = colReduce(uGrid, i, xPremise[i])
                uGrid = tbtReduce(uGrid, i, xPremise[i])
        xPremise, uGrid = lookForSingleUs(uGrid)
        uTotal1 = checkUTotal(uGrid)
    return xPremise, uGrid

def checkForInitialContradictions(uGrid):
    # check that uGrid matches for cells where the premise is given
    # check that there are no contradictions immediately upon first initialization
    return

def printGrid(g, desc):
    print(desc)
    print(g[:9])
    print(g[9:18])
    print(g[18:27])
    print(g[27:36])
    print(g[36:45])
    print(g[45:54])
    print(g[54:63])
    print(g[63:72])
    print(g[72:])
    return

def isSolved(uGrid):
    for cell in uGrid:
        if len(cell) != 1:
            return False
    return True

def justBruteForceTheRest(premise, uGrid):
    premiseW = premise
    uGridW = uGrid
    solved = False
    noCon = True
    for cell in range(len(uGridW)):
        # reset grid to state at start of brute force permutations
        uGridTemp = uGridW
        premiseTemp = premiseW
        if len(uGridW[cell]) != 1:
            for v in uGridW[cell]:
                if solved == False:
                    premiseTemp = premiseW
                    uGridTemp = uGridW
                    print("trying " + str(v) + " in cell " + str(cell))
                    #input()
                    
                    # try one of the u-values
                    premiseTemp[cell] = v
                    
                    # reduce the u-grid based on this trying value
                    premiseTemp, uGridTemp = initializeUGrid(premiseTemp)
                    printGrid(uGridTemp, "")
                    
                    # if this resulted in a contradiction, move on to the next trying u-value
                    print("checking for contradictions")
                    
                    if checkForContradictions(uGridTemp) == True:
                        print("contradiction found")
                        # return premiseTemp, uGridTemp, False, False
                        continue
                    
                    # if this did not result in a contradiction, try the next unsolved cell
                    print("no contradiction found")
                    
                    if checkForContradictions(uGridTemp) == False:
                        if isSolved(uGridTemp):
                            print("solution found")
                            printGrid(premiseTemp, "")
                            return premiseTemp, uGridTemp, True, True
                        premiseTemp, uGridTemp, solved, noCon = justBruteForceTheRest(premiseTemp, uGridTemp)
                if solved == True:
                    return premiseTemp, uGridTemp, True, True
    print("something weird happened if we got to this point")
    return premiseTemp, uGridTemp, solved, noCon

def checkForContradictions(uGrid):
    for cell in uGrid:
        if len(cell) == 0:
            return True
    return False


premise, uGrid = initializeUGrid(premise)
printGrid(premise, "grid state after initialization and first reduction")
printGrid(uGrid, "initialized and reduced uGrid")

if checkUTotal(uGrid) > 81:
    print("brute force the rest...")
    premise, uGrid, done, noCon = justBruteForceTheRest(premise, uGrid)
    # printGrid(premise, "final grid state")
else:
    print("done... no solution found")

# to do
# //// check for empty cells in uGrid (contradictions)