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
print(premise[0:8])
print(premise[9:17])
print(premise[18:26])
print(premise[27:35])
print(premise[36:44])
print(premise[45:53])
print(premise[54:62])
print(premise[63:71])
print(premise[72:80])



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
    for x in uGrid:
        if len(x) == 1:
            premise += [x]
        else:
            premise += [" "]
    return premise

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
    uTotal0 = checkUTotal(uGrid) # initialize uTotal (total potential values in grid)
    uTotal1 = 10*81
    while uTotal1 > uTotal0:
        print("debug")
        for i in range(len(xPremise)):
            if xPremise[i] != " ":
                uGrid = rowReduce(uGrid, i, xPremise[i])
                uGrid = colReduce(uGrid, i, xPremise[i])
                uGrid = tbtReduce(uGrid, i, xPremise[i])
        xPremise = lookForSingleUs(uGrid)
        uTotalNew = checkUTotal(uGrid)
    return xPremise, uGrid


premise, uGrid = initializeUGrid(premise)
print("grid state after initialization and first reduction")
print(premise[0:8])
print(premise[9:17])
print(premise[18:26])
print(premise[27:35])
print(premise[36:44])
print(premise[45:53])
print(premise[54:62])
print(premise[63:71])
print(premise[72:80])

print("initialized and reduced uGrid")
print(uGrid[0:8])
print(uGrid[9:17])
print(uGrid[18:26])
print(uGrid[27:35])
print(uGrid[36:44])
print(uGrid[45:53])
print(uGrid[54:62])
print(uGrid[63:71])
print(uGrid[72:80])



# to do
# //// check for empty cells in uGrid (contradictions)