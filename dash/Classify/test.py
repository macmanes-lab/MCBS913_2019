import sys, os
from Node import Node
from concurrent.futures import ThreadPoolExecutor
from Tree import Tree
import time
import random
tree = Tree()

#
def processQuery(query, distance):
    tree.add(query, distance)
#
# def task(item):
#     print(item)

def main():


    start = time.time()
    fileName = sys.argv[1]
    for line in open(fileName):
        distance, full_tax = line.rstrip().split('\t')
        query = full_tax.split(':')[1:]

        processQuery(query,distance)

    # list = [1,2,3,4]
    # exe = ThreadPoolExecutor(max_workers=4)
    #
    # for fur in exe.map(task,list):
    #     print("finish")
    # print("Time", time.time() - start)
    #
    # leafdir = tree.getNode("Pseudomonas").getLeafDir()
    # print(len(leafdir))
    # for key, value in leafdir.items():
    #     print(key)
    #     print(value.getName())

    print(tree.randomPick(15))

    #print(tree.getNode("_root").getLevel())
    # tree.generateLevel()
    # print(tree.getNode("Pseudomonas aeruginosa").getLevel())
    # print(tree.getLevel())


if __name__== "__main__":
    main()