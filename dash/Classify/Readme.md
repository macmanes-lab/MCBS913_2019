# Document for Classify package

In this package, Classify.py runs under Python3. Take a data file's full path as argument(fowlling by Classify.py). Also make sure run under the Classify package.

Example:

```bash
Python3 Classify.py test_data.txt
```

## **Idea**

The implement idea in this package is to node to represent every entity from the data file. Based on the order from data file, a tree was consisted by these node. Every node has the necessary attributes like the distance list and who is its children.

## **Node.py**

This is a class to represent the node in the Tree

**getName()**: Return the curret node instace's name

**getChildren()**: Return all of the current node instance's children as a dictionary

**getDistance(**): Return all of the current node's distance as a list. The distance is the everyline's leading number in data file.

**addChild(key,value)**:This method add  another node instance to the current instance's children dirctionay. The key is children's name in string, value is the node instance which is an object of Node class. The reason to use dictionary rather than list is the time complexity for dictionary search is constant. List is O(n)

**addDistance(distance)**: Append a distance to the current node instance's distance list

## **Tree.py**

This is a class to represent the whole structure from the data file. Every entity is a node object from Node class.

**add(query,distance):** This method take query list and distance number as argument. Recursively search the right position to insert the new node.

@Parameters 

query: A list get from data file. Eg:['Eukaryota', 'Viridiplantae', 'Streptophyta', 'Liliopsida', 'Poales', 'Poaceae', 'Aegilops', 'Aegilops tauschii']

distance: the each line's leading number of the data file

**addHelper(index,query,parent,distance)**: Helper function to impelement recursion.Basically, user may not want to change code in this function

@Parameters

Index: query list's index

parent: current pointed node 's parent node'

distance:the each line's leading number of the data file

**printTree():** A fuction to print all paths from root to lowest leaf.

**DFS(root,allPath,path):** Help function to impelement printTree() by Depth First Search algrihom.User may not want to change this method

@Parameter

allPath: A nested list to store all paths

path: A list to store one path from root to leaf

**getPathDir()**: Return all paths as a directory

**getAllPath()**:Return all paths as a list

**getTotalNodes()**: Return all TreeNode as a directory, key is the node's name, value is the node instance

**getRoot(): ** Return the root node. The returned root node is the dummy node. Every useful node is starting from this root's children

**size():**Return tree size: how many tree node in this tree

**getNode(name):**Return a specific tree node instance by name in string type

**getDistance(query)**: Return a dictionary. Key is entity in query  like "Eukaryota", value is the distance list

the query list like['Eukaryota', 'Viridiplantae', 'Streptophyta', 'Liliopsida', 'Poales', 'Poaceae', 'Aegilops', 'Aegilops tauschii']

**getDistanceByName(self,name):** Return a distance list by name in string type



## Classify.py

The script basically create an instance of Tree class, read input data file. Use the Tree's method

