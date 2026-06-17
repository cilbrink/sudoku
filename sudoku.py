import math

debug = []
for x in range(32):
    debug += [False]

# use temporary debug grid (not user-input)
debug[0] = True
# use NYT 2026-06-15 medium (=False) or hard (=True) puzzle
debug[1] = False


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
        if debug[1] == False:
            pass
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
                "3"," "," ","6"," "," "," ","7"," "]
        if debug[1] == True:
            pass
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
                " "," ","3"," "," "," "," ","8","7"]
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
        print("debug")
        uTotal0 = uTotal1
        for i in range(len(xPremise)):
            if xPremise[i] != " ":
                uGrid = rowReduce(uGrid, i, xPremise[i])
                uGrid = colReduce(uGrid, i, xPremise[i])
                uGrid = tbtReduce(uGrid, i, xPremise[i])
        xPremise, uGrid = lookForSingleUs(uGrid)
        uTotal1 = checkUTotal(uGrid)
    return xPremise, uGrid


premise, uGrid = initializeUGrid(premise)
print("grid state after initialization and first reduction")
print(premise[:9])
print(premise[9:18])
print(premise[18:27])
print(premise[27:36])
print(premise[36:45])
print(premise[45:54])
print(premise[54:63])
print(premise[63:72])
print(premise[72:])

print("initialized and reduced uGrid")
print(uGrid[:9])
print(uGrid[9:18])
print(uGrid[18:27])
print(uGrid[27:36])
print(uGrid[36:45])
print(uGrid[45:54])
print(uGrid[54:63])
print(uGrid[63:72])
print(uGrid[72:])



# to do
# //// check for empty cells in uGrid (contradictions)