#! python3
from __future__ import division

import copy
from Node import Node
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import random
import time


class Tree:

    # to initial necessary vairable
    def __init__(self):
        self._root = Node("root")
        self.totalNodes = {"_root": self._root}
        self._size = 0
        self.totalPath = []
        self.dir = {}
        self._levelFlag = False
        self._levels = 0


    # print out the tree by all paths from root to leaf
    def printTree(self):

        print("============================Print tree")
        allPath = []
        path = []
        self.DFS(self._root,allPath,path)
        self.totalPath = allPath
        # for x in allPath:
        # 	self.totalPath.append(''.join(x))
        # 	self.dir[''.join(x)] = 0
        for x in self.totalPath:
            print(x)

    # return all paths as a directory
    def getPathDir(self):
        return self.dir

    # return all paths as a list
    def getAllPath(self):
        return self.totalPath

    # return all TreeNode as a directory
    def getTotalNodes(self):
        return self.totalNodes


    # Help function of print the tree. Impemented by Depth first search recursivly
    def DFS(self,root,allPath,path):
        #print(type(root))

        #print(root.getName())
        childrenList = root.getChildren()
        if len(childrenList) == 0:
            allPath.append(copy.deepcopy(path))
            return

        for k,v in childrenList.items():
            path.append(v.getName())
            self.DFS(v,allPath,path)
            path.pop()


    # return the root node
    def getRoot(self):
        return self._root

    # return tree size: how many tree node in this tree
    def size(self):
        return self._size

    # return a specific tree node by name
    def getNode(self,name):
        return self.totalNodes.get(name)

    def multiThreadingAddLeaf(self,nodeName):
        node = self.totalNodes.get(nodeName)
        node.addLeaf(leafName, leafNode)


    # add node to the tree. argument include the query list and the query list's distance
    def add(self,query,distance):

        self.addHelper(0,query,self._root,distance)

        querySize = len(query)

        # exe = ThreadPoolExecutor(max_workers=1)
        global leafName
        leafName = query[querySize-1]
        global leafNode
        leafNode = self.totalNodes.get(leafName)

        #print(leafName)
        # for fur in exe.map(self.multiThreadingAddLeaf,query):
        #     pass

        node = self._root

        for index in range(0,querySize-1):
            node = node.getChildren().get(query[index])
            node.addLeaf(leafName,leafNode)


    # add helper function, recursivly find the position to insert the node
    def addHelper(self,index,query,parent,distance):
        if index == len(query):
            parent.addDistance(float(distance))
            return
        node = parent.getChildren().get(query[index])

        if node == None:
            newNode = Node(query[index])
            self.totalNodes[query[index]] = newNode
            parent.addChild(newNode.getName(),newNode)
            parent.addDistance(float(distance))
            self._size += 1
            index += 1
            self.addHelper(index,query,newNode,distance)
            return

        else:
            parent.addDistance(float(distance))
            index += 1
            self.addHelper(index,query,node,distance)
            return

    # testing function.
    # def testFuc(self):
    # 	for k,v in self.totalNodes["Eukaryota"].getChildren().items():
    # 		print(k,end=" ")


    # 	print("for B")

    # 	for k,v in self.totalNodes["Bacteria"].getChildren().items():
    # 		print(k,end=" ")

    # this is also testing function
    def check(self,query):
        index = 0
        childrenList = self._root.getChildren()

        while index < len(query):
            node = childrenList.get(query[index])

            if node == None:
                return False
            else:
                node = childrenList.get(query[index])
                childrenList = node.getChildren()
                index +=1
        return True



    """
    function: Argument:the query list like['Eukaryota', 'Viridiplantae', 'Streptophyta', 'Liliopsida', 'Poales', 'Poaceae', 'Aegilops', 'Aegilops tauschii']
    return a directory where the key is the name like "Eukaryota",the value is the distance list
    """
    def getDistance(self,query):
        distanceDir={}
        for x in query:
            distanceDir[x] = self.totalNodes[x].getDistance()

        return distanceDir

    def getDistanceByName(self, name):
        node = self.totalNodes[name]
        if node is None:
            print("No such element")
        else:
            return node.getDistance()

    # level order traversal. To go throught every node,
    # print out the children name which has highest distance value
    def getMaxDistFromChildren(self):
        q = Queue()
        for k,v in self._root.getChildren().items():
            q.put(v)
        print("=======================================================")
        print("Patten: Parent: maxDistance : children with max distance")
        print("=======================================================")
        print("")
        while not q.empty():
            size = q.qsize()
            for x in range(size):
                node = q.get()
                if len(node.getChildren()) == 0:
                    continue
                print(node.getName(), ' :', end=" ")
                maxSocre = 0.0

                nameList = []
                for subK,subV in node.getChildren().items():
                    distanceList = subV.getDistance()
                    score  = max(distanceList)
                    if score >= maxSocre:
                        maxSocre = score
                        nameList.append(subK)
                    q.put(subV)
                print(" ", str(maxSocre), " : ", nameList)

    def getMaxDistPath(self):

        node = self._root
        maxDistance = 0
        path = []
        distance = []
        while len(node.getChildren()) != 0:
            # print(path);
            # print(len(node.getChildren()))
            for k, v in node.getChildren().items():

                if v.getMaxDistance() > maxDistance:
                    node = v
                    maxDistance = v.getMaxDistance()

            path.append(node.getName())
            distance.append(maxDistance)
            maxDistance = 0
        # print(node.getName())

        print(path);
        # print(distance)
        return path

    def generateLevel(self):
        q = Queue()

        q.put(self._root)

        while not q.empty():
            self._levels += 1
            size = q.qsize()
            for i in range(size):

                item = q.get()

                for k,v in item.getChildren().items():
                    v.setLevel(self._levels)
                    q.put(v)

    def getLevel(self):
        return self._levels

    def randomPick(self,N):
        if self._levelFlag == False:
            self.generateLevel()
            self._levelFlag == True

        return self.randomPickHelper(self._root,N)

    def randomPickHelper(self,node,N):
        if self._levelFlag == False:
            self.generateLevel()
            self._levelFlag == True

        pickedList = []

        q = Queue()
        q.put((node,N))
        while not q.empty():
            size = q.qsize()

            for i in range(size):
                item, target = q.get()

                print(item.getName())
                childNum = item.childrenSize()

                if childNum <= target:
                    remainder = target % childNum
                    unit = target // childNum

                    for childName, childNode in item.getChildren().items():

                        if remainder > 0:
                            tmp = unit + 1
                            remainder -= 1

                        else:
                            tmp = unit

                        if childNode.getLevel() == self._levels -2:

                            if(childNode.leafSize() <= tmp):
                                for k, v in childNode.getLeafDir().items():
                                    if pickedList.contains(k):
                                        continue
                                    pickedList.append(k)
                            else:
                                for i in range(tmp):
                                    pickedName = random.choice(list(childNode.getLeafDir()))

                                    if pickedName in pickedList:
                                        for i in range(len(list(childNode.getLeafDir()))):
                                            pickedName = random.choice(list(childNode.getLeafDir()))
                                            if pickedName not in pickedList:
                                                pickedList.append((pickedName))
                                                break
                                    else:
                                        pickedList.append(pickedName)
                            continue

                        if childNode.leafSize() <= tmp:

                            for k,v in childNode.getLeafDir().items():
                                if pickedList.contains(k):
                                    continue
                                pickedList.append(k)
                        else:
                            q.put((childNode,tmp))
                #randomly pick target
                else:

                    if item.getLevel() == self._levels - 2:
                        for i in range(min(target,childNum)):
                            pickedName = random.choice(list(item.getLeafDir()))
                            if pickedName in pickedList:
                                for i in range(len(list(item.getLeafDir()))):
                                    pickedName = random.choice(list(item.getLeafDir()))
                                    if pickedName not in pickedList:
                                        pickedList.append((pickedName))
                                        break
                            else:
                                pickedList.append(pickedName)

                    elif item.getLevel() == self._levels -1 :
                        continue
                    else:
                        for i in range(target):
                            # tmpList = item.getChildren()
                            tmpNode = item.getChildren().get(random.choice(list(item.getChildren())))

                            pickedName = random.choice(list(tmpNode.getLeafDir()))
                            if pickedName in pickedList:
                                for i in range(len(list(tmpNode.getLeafDir()))):
                                    pickedName = random.choice(list(tmpNode.getLeafDir()))
                                    if pickedName not in pickedList:
                                        pickedList.append((pickedName))
                                        break
                            else:
                                pickedList.append(pickedName)
        return pickedList