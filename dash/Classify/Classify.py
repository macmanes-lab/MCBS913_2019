#! python3
import sys
from Tree import Tree
from Node import Node
import statistics

tree = Tree()

def processQuery(query,distance):
	tree.add(query,distance)


#total classify sequence
def classify_sequence(totalNodes):
	totalNodes.pop("_root")
	taxon = ''
	top_score = 0.0
	#k is name in string type, v is node instance
	for k,v in totalNodes.items():
		distanceList = v.getDistance()
		score = max([float(x) for x in distanceList])
		score = statistics.median([float(x) for x in distanceList])
		print(k,score,sorted(distanceList,reverse=True))
		if score > top_score:
			top_score = score
			taxon = k

	return taxon

def classify_sequenceByName(name):
	distanceList = tree.getDistanceByName(name)
	taxon = ''
	top_score = 0.0
	score = max([float(x) for x in distanceList])
	score = statistics.median([float(x) for x in distanceList])
	print(k,score,sorted(distanceList,reverse=True))




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

	#print(tree.getDistanceByName("Eukaryota"))
	totalNodes = {}
	totalNodes = tree.getTotalNodes()
	#classify_sequence(totalNodes)
	tree.getMaxDistFromChildren()

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
