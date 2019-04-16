#! python3

class Node:
    def __init__(self, name):
        self._name = name
        self._children = {}
        self._distance = []
        self._leaf = {}
        self._level = 0


    def getName(self):
        return self._name

    def getChildren(self):

        return self._children

    def childrenSize(self):
        return len(self._children)

    def getDistance(self):
        return self._distance

    # store the instance's child in a dictonary
    def addChild(self, key,value):
        self._children[key] = value

    # append the distance
    def addDistance(self, distance):
        self._distance.append(distance)

    # get max distance of children
    def getMaxDistance(self):
        # return max(self._distance)
        return max([float(x) for x in self._distance])

    def addLeaf(self,leafName, leaf):
        self._leaf[leafName] = leaf

    def leafSize(self):
        return len(self._leaf)
    def getLeafDir(self):
        return self._leaf

    def setLevel(self,level):
        self._level = level
    def getLevel(self):
        return self._level