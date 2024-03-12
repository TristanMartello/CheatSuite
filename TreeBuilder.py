from wordTree import wordNode
from wordList import words as wordList

# Process word bank
#   - Iterate through each word building a tree
#   - Each node level is a new possible next letter
#   - Possibly have each node contain a list of children- easy scanning for next move
#   - Each node has boolean value indicating 'end of word' or not
def createWordTree():
    root = wordNode(None)
    for word in wordList:
        recursiveAddWord(word, root)
    return root

# Add each word letter by letter into the tree recursively
def recursiveAddWord(word, parent):
    if len(word) == 0:
        parent.markFinal()
        return
    else:
        currLetter = word[0]
        child = parent.addChild(currLetter)
        return recursiveAddWord(word[1:], child)
