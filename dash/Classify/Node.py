#! python3

class Node:
	def __init__(self,name):
		self._name = name
		self._children = {}
		self._distance = []


	def getName(self):
		return self._name

	def getChildren(self):

		return self._children

	def getDistance(self):
		return self._distance


	#store the instance's child in a dictonary
	def addChild(self,key,value):
		self._children[key] = value

	#append the distance
	def addDistance(self,distance):
		self._distance.append(distance)



