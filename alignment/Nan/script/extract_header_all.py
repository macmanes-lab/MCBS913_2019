### extract all headers from reference fasta file

import re
inputFile = open('../reference/repdb_new.fasta', 'r')
doc=open('head_all.txt','w')
j = 0

for line in inputFile:   
	matchg = re.match(r'(>)(.*)',line,re.M|re.I)
	if matchg:
		s = ""
		s += matchg.group(2)
		print(s, file=doc)
		## j=j+1
		## if j == 5:
			## break	
inputFile.close()
doc.close()
 