from TreeBuilder import createWordTree

MIN_WORD_LEN = 4
MAX_WORD_LEN = 4
GRID_SIZE = 4
ANSWER_DICT = {}

def getGridSize():
    global GRID_SIZE
    proceed = False
    while not proceed:
        try:
            gridInput = int(input("Enter Grid Size: "))
            if gridInput > 1:
                GRID_SIZE = gridInput
                proceed = True
        except:
            print("Input must be a number")
    
# Obtain and refotmat input grid of letters
#   - ABCD,EFGH,IJKL,MNOP format perhaps
def getSquare():
    proceed = False
    while not proceed:
        print("Format: ABCD-EFGH-IJKL-MNOP")
        squareString = input("Enter Square: ")
        items = squareString.lower().split("-")
        error = False
        for line in items:
            if len(line) != GRID_SIZE or not line.isalpha():
                error = True
        if not error:
            proceed = True
        if len(items) != GRID_SIZE:
            proceed = False
    
    square = []
    for row in range(GRID_SIZE):
        newRow = []
        for col in range(GRID_SIZE):
            newRow.append(items[row][col])
        square.append(newRow)

    return square

def getMaxLen():
    global MAX_WORD_LEN
    proceed = False
    while not proceed:
        try:
            maxLen = int(input("Enter length of longest word: "))
            if maxLen > 3 and maxLen < GRID_SIZE**2:
                proceed = True
                MAX_WORD_LEN = maxLen
            else:
                print("Number must be between 4 and 16")
        except:
            print("Entry must be a number")

# Iterate through every combination, comparing with wordlist
#  - For each possible next move, see if curr/next letter combo is
#    represented with curr/child nodes
#  - For each chain, track both terminal nodes and possible continuations
def makeAnswerDict():
    global ANSWER_DICT
    for i in range(MIN_WORD_LEN, MAX_WORD_LEN + 1):
        ANSWER_DICT[i] = []

def inRange(coord):
    return coord >= 0 and coord < GRID_SIZE

# Return a list of all spots adjacent to the current position
def getAdjCoords(currPos):
    adjCoords = []
    for rowMod in [-1, 0, +1]:
        for colMod in [-1, 0, +1]:
            if inRange(currPos[0] + rowMod) and inRange(currPos[1] + colMod):
                adjCoords.append([currPos[0] + rowMod, currPos[1] + colMod])
    return adjCoords

# Get the list of all adjacent letters, then remove ones that have been traversed
def getValidCoords(prevCoords):
    adjCoords = getAdjCoords(prevCoords[-1])
    for usedCoords in prevCoords:
        if usedCoords in adjCoords:
            adjCoords.remove(usedCoords)
    return adjCoords

def isValidLen(strLen):
    return strLen >= MIN_WORD_LEN and strLen <= MAX_WORD_LEN

def recursiveGridSearch(square, currLetter, prevString, prevCoords, currParent):
    global ANSWER_DICT
    # Ensure current letter is a valid path from previous one according to tree
    currNode = currParent.checkChild(currLetter)
    if currNode is not None:
        currString = prevString + currLetter
        # If this letter is a potential word ender, and the length is right, add to dictionary
        if currNode.final and isValidLen(len(currString)):
            if currString not in ANSWER_DICT[len(currString)]:
                ANSWER_DICT[len(currString)].append(currString)

        # Get list of all possible (legal) next moves
        validCoords = getValidCoords(prevCoords)

        # For each possible next move, continue searching
        for coords in validCoords:
            newLetter = square[coords[0]][coords[1]]
            newCoords = prevCoords + [coords]
            recursiveGridSearch(square, newLetter, currString, newCoords, currNode)

def theBigGun(wordRoot, square):
    makeAnswerDict()

    # Iterate through every square as a starter and launch a recursive search through the grid
    for row in range(len(square)):
        for col in range(len(square[0])):
            letter = square[row][col]
            recursiveGridSearch(square, letter, "", [[row, col]], wordRoot)

# Output final list of words- with confidence?
def displayAnswers():
    if ANSWER_DICT is not None:
        for key in ANSWER_DICT:
            if len(ANSWER_DICT[key]) > 0:
                print(key, "LETTER WORDS (" + str(len(ANSWER_DICT[key])) + "):")
                sorted = ANSWER_DICT[key]
                sorted.sort()
                for word in sorted:
                    print("  - " + word)
    else:
        print("No valid words found")

def main():
    root = createWordTree()
    #root.printAllWords("")

    getGridSize()
    square = getSquare()
    getMaxLen()
    print("Great.")

    theBigGun(root, square)
    displayAnswers()

main()
