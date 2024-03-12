
# Tree implementation
#  - Each node represents the next possible letter for a word
#  - Each node tracks the current letter, a list of children,
#    a list of children's letters, and a boolean indicating
#    if this is a possible last letter for a word


class wordNode:
    def __init__(self, selfLetter, finalBool=False):
        self.letter = selfLetter
        self.children = []
        self.childLetters = []
        self.final = finalBool

    # Indicate that this is a valid ending letter for a word
    # Returns nothing
    def markFinal(self):
        self.final = True
    
    # Add a child to the current node
    # Returns the child node
    def addChild(self, newLetter):
        if newLetter in self.childLetters:
            return self.children[self.childLetters.index(newLetter)]
        else:
            newChild = wordNode(newLetter)
            self.childLetters.append(newLetter)
            self.children.append(newChild)
            return newChild

    # Check child sees if the requested child of the current node exists
    # returns the node if it exists, and None if not
    def checkChild(self, newLetter):
        if newLetter in self.childLetters:
            return self.children[self.childLetters.index(newLetter)]
        else:
            return None

    # This is basically a depth first search through the tree
    def printAllWords(self, currWord):
        pLetter = "" if self.letter is None else self.letter
        currWord += pLetter
        
        for child in self.children:
            child.printAllWords(currWord)

        if not self.children:
            print(currWord)
