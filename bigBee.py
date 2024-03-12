
from TreeBuilder import createWordTree

ANSWER_DICT = {}
PANGRAMS = []
MIN_WORD_LEN = 4
MAX_WORD_LEN = 16
KEY_LETTER = ""

def getWordHex():
    global KEY_LETTER
    proceed = False
    while not proceed:
        print("Format: ABCDEFG, first letter is center")
        wordHex = input("Enter Hex: ")
        if len(wordHex) == 7 and wordHex.isalpha():
            proceed = True
        else:
            print("Must input a string of seven characters")
    wordHex = wordHex.lower()
    KEY_LETTER = wordHex[0]
    return wordHex

def makeAnswerDict():
    global ANSWER_DICT
    for i in range(MIN_WORD_LEN, MAX_WORD_LEN + 1):
        ANSWER_DICT[i] = []

# Word finding algorithm
#  - Pick a start letter
#  - Test a second letter from the list (including self)
#  - See if path exists on tree
#     - If so, continue recursing to next step
#        - If current node is final, check if word contains center letter
#        - If so, add to dictionary
#     - If not, abandon path

def beginSearch(wordHex, root):
    for letter in wordHex:
        recursiveSearch(wordHex, letter, "", root)

def recursiveSearch(wordHex, currLetter, prevWord, currParent):
    global ANSWER_DICT, PANGRAMS
    currNode = currParent.checkChild(currLetter)
    # If current word exists on some path
    if currNode is not None:
        currWord = prevWord + currLetter

        # If this letter is a possible word end, verify and add
        if currNode.final and isValid(currWord):
            if currWord not in ANSWER_DICT:
                ANSWER_DICT[len(currWord)].append(currWord)
            if isPangram(wordHex, currWord):
                PANGRAMS.append(currWord)
        
        # Iterate through all possible next letters
        for newLetter in wordHex:
            recursiveSearch(wordHex, newLetter, currWord, currNode)

def isValid(word):
    return len(word) >= MIN_WORD_LEN and len(word) <= MAX_WORD_LEN and KEY_LETTER in word

def isPangram(wordHex, word):
    for letter in wordHex:
        if letter not in word:
            return False
    return True

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

def displayPangrams():
    print("\nPangrams(!!!):")
    for word in PANGRAMS:
        print("  -", word)

def main():
    # Load in word tree
    root = createWordTree()

    # Build answer dictionary
    makeAnswerDict()

    # Obtain user input
    wordHex = getWordHex()

    # Search the grid to get every word possible
    beginSearch(wordHex, root)

    displayAnswers()
    displayPangrams()

main()