###extract header of bacteria from reference fasta file

import re
inputFile = open('../reference/repdb_new.fasta', 'r')
doc=open('bac_head.txt','w')
j = 0

for line in inputFile:   
	matchg = re.match(r'(>)(.*\|bacteria.*)',line,re.M|re.I)
	if matchg:
		s = ""
		s += matchg.group(2)
		print(s, file=doc)
		## j=j+1
		## if j == 5:
			## break	
inputFile.close()
doc.close()
 