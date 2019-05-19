import re

BOWTLOG = '../../bowtie_Mock_output/Mock_small_even_output.sam'

def convert_line_sta(line):
    tempLine = line.split('\t')
    res = ""
    if READTOKEN in tempLine[0]:
        res += tempLine[0] + " "
        res += tempLine[2]
    return res

output = open('bt_even.txt', 'w')
with open(BOWTLOG, buffering=2000000000) as f:
    for line in f:
        temp = []
        temp = convert_line_sta(line)
        if temp != "":
            output.write(str(temp)+'\n')
        #         j += 1
        # if j == 1000:
        #         break
