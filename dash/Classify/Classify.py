#! python3
import sys
from Tree import Tree
from Node import Node
import statistics

tree = Tree()

def processQuery(query,distance):
	tree.add(query,distance)


def main():

	# if sys.argv[1] == "-help" or sys.argv[1] == "-h" or sys.argv[1] == "-H" :
	# 	print("usage: python Classify.py [Data File]")
	# 	return
	fileName = sys.argv[1]
	original = []
	count = 1
	for line in open(fileName):
		distance,full_tax = line.rstrip().split('\t')
		query = full_tax.split(':')[1:]
		#print(distance,query)
		count+=1
		original.append(query)
		processQuery(query,distance)

	print(tree.getDistanceByName("Eukaryota"))

	#tree.printTree()


	# treePathDir = tree.getPathDir()
	# treeAllPath = tree.getAllPath()

	# checking(original,treePathDir,treeAllPath)
	# diff = 0
	# for x in original:

	# 	flag = tree.check(x)
	# 	if flag ==False:
	# 		diff += 1

	# for x in original:
	# 	print(x)
	# 	tmp = tree.getDistance(x)
	# 	for k,v in tmp.items():
	# 		print(k,v)

	# print(diff)
	# tree.testFuc()



if __name__== "__main__":
	main()
