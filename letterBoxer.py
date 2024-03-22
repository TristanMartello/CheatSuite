from TreeBuilder import createWordTree

MIN_WORD_LEN = 3
MAX_WORD_LEN = 15
GRID_LEN = 3
WORD_NUM_CUTOFF = 0

def getBox():
    proceed = False
    while not proceed:
        print("Use this format: ABC-DEF-JHI-JKL")
        boxInput = input("Enter word box: ")
        items = boxInput.lower().split("-")
        error = False
        for side in items:
            if len(side) != GRID_LEN or not side.isalpha():
                error = True
        if not error:
            proceed = True
        if len(items) != 4:
            proceed = False
    
    box = []
    for row in range(4):
        newRow = []
        for col in range(GRID_LEN):
            newRow.append(items[row][col])
        box.append(newRow)
    print(box)
    return box

def getMaxLen():
    global WORD_NUM_CUTOFF
    proceed = False
    while not proceed:
        try:
            maxLen = int(input("Enter number of words in chain: "))
            if maxLen > 1 and maxLen < 7:
                proceed = True
                WORD_NUM_CUTOFF = maxLen
            else:
                print("Number must be between 4 and 16")
        except:
            print("Entry must be a number")


#  LETTER BOXED RULES
#   - Use up all letters in a chain of words
#   - Each word's ending letter starts the next word
#   - All words are at least 3 letters
#   - Consecutive letters cannot be on the same side
#   - No repeated letters

# Search algo for this:
#  Loop through each letter as a possible starter with no curr word
#    - For each curr Letter:
#      - See if prevWord + currLetter is in tree
#        - If not, abort
#        - If it is:
#           - If currLetter is a possible ender, try splitting words here, using currLetter as starter
#           - Continue recursing on all new possible words and prevWord + currLetter as prevWord

def beginSearch(wordBox, root):
    for sideNum in range(len(wordBox)):
        for letter in wordBox[sideNum]:
            taken = [[], [], [], []]
            currSol = []
            recursiveSearch(wordBox, sideNum, currSol, "", letter, root, taken, root)

# Create deep copy of word list
def deepCopy(startList):
    newList = []
    for item in startList:
        newList.append(item)
    return newList

# Create deep copy of a list of lists
def doubleDeepCopy(startList):
    newList = []
    for subList in startList:
        newSub = deepCopy(subList)
        newList.append(newSub)
    return newList

def recursiveSearch(wordBox, currSide, currSol, prevWord, currLetter, currParent, taken, root):
    currNode = currParent.checkChild(currLetter)
    if currNode is not None:
        currWord = prevWord + currLetter
        
        # Track the current letter being used
        taken = trackTaken(taken, currSide, currLetter)
        
        if currNode.final and len(currWord) >= MIN_WORD_LEN and len(currWord) <= MAX_WORD_LEN:
            if currWord not in currSol:
                # If this could be the last letter, try ending the word here
                currSol.append(currWord)

                # If this could complete the puzzle, check
                if isEqual(wordBox, taken, currSol):
                    print(currSol)
                else:
                    # If it doesn't, start searching for new words
                    modSol = deepCopy(currSol)
                    newTaken = doubleDeepCopy(taken)
                    recursiveSearch(wordBox, currSide, modSol, "", currLetter, root, newTaken, root)
        
        # If current solution is more that 5 words, abort
        if len(currSol) < WORD_NUM_CUTOFF:
            # If current word is not complete, recurse to build the word
            for rowNum in range(len(wordBox)):
                if rowNum != currSide:
                    for letter in wordBox[rowNum]:
                        modSol = deepCopy(currSol)
                        newTaken = doubleDeepCopy(taken)
                        recursiveSearch(wordBox, rowNum, modSol, currWord, letter, currNode, newTaken, root)

def trackTaken(taken, currSide, currLetter):
    if currLetter not in taken[currSide]:
        taken[currSide].append(currLetter)
    return taken

def isEqual(wordBox, solBox, currSol):
    if len(solBox) != 4:
        return False
    for row in solBox:
        if len(row) != GRID_LEN:
            return False

    for sideNum in range(4):
        side = wordBox[sideNum]
        for letter in side:
            if letter not in solBox[sideNum]:
                return False

    return True
    
def main():
    # Build word tree
    root = createWordTree()

    # Build word box
    box = getBox()

    # Find length of word string
    getMaxLen()

    # Engage
    beginSearch(box, root)

main()

# WBS-KLZ-ADY-ECR
# RVH-EAI-WNP-OMG