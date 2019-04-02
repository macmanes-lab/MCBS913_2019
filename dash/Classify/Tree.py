#! python3
import copy
from Node import Node
import queue


class Tree:

	#to initial necessary vairable
	def __init__(self):
		self._root = Node("root")
		self.totalNodes = {}
		self.totalNodes["_root"] = self._root
		self._size = 0
		self.totalPath = []
		self.dir = {}


	#print out the tree by all paths from root to leaf
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

	#return all paths as a directory
	def getPathDir(self):
		return self.dir

	#return all paths as a list
	def getAllPath(self):
		return self.totalPath

	#return all TreeNode as a directory
	def getTotalNodes(self):
		return self.totalNodes


	#Help function of print the tree. Impemented by Depth first search recursivly
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


	#return the root node
	def getRoot():
		return self._root

	#return tree size: how many tree node in this tree
	def size(self):
		return self._size

	#return a specific tree node by name
	def getNode(self,name):
		return totalNodes.get(name)

	#add node to the tree. argument include the query list and the query list's distance
	def add(self,query,distance):

		self.addHelper(0,query,self._root,distance)

	#add helper function, recursivly find the position to insert the node
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

	#testing function.
	# def testFuc(self):
	# 	for k,v in self.totalNodes["Eukaryota"].getChildren().items():
	# 		print(k,end=" ")


	# 	print("for B")

	# 	for k,v in self.totalNodes["Bacteria"].getChildren().items():
	# 		print(k,end=" ")

	#this is also testing function
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
	def getDistanceByName(self,name):
		node = self.totalNodes[name]
		if node == None:
			print("No such element")
		else:
			return node.getDistance()

	#level order traversal. To go throught every node,
	#print out the children name which has highest distance value




	def getMaxDistFromChildren(self):
		q = queue.Queue()
		for k,v in self._root.getChildren().items():
			q.put(v)
		print("=======================================================")
		print("Patten: Parent: maxDistance : children with max distance")
		print("=======================================================")
		print("")
		while q.empty() == False:
			size = q.qsize()
			for x in range(size):
				node = q.get()
				if len(node.getChildren()) == 0:
					continue
				print(node.getName(),' :',end = " ")
				maxSocre = 0.0

				nameList = []
				for subK,subV in node.getChildren().items():
					distanceList = subV.getDistance()
					score  = max(distanceList)
					if score >= maxSocre:
						maxSocre = score
						nameList.append(subK)
					q.put(subV)
				print(" ",str(maxSocre)," : ",nameList)

	def getMaxDistPath(self):

		node = self._root
		maxDistance = 0
		path = {}
		distance = {}
		while node.getChildren() != None:
			for k,v in node.getChildren().items():
				if v.getMaxDistance() > maxDistance:
					node = v
					maxDistance =  v.getMaxDistance()
					path.append(v.getName())
					distance.append(v.getMaxDistance())
