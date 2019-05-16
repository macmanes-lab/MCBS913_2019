# Original log.sam outputed by Bowtie
BOWTLOG = 'Mock_bac_sub_log_output.sam'

# All reads begin with 'ERR' used to verify if a line is header or content
READTOKEN = "ERR"

# Extract ReadName/ReadID from each line
def extract_ID_S(taxonomy):
    temp = taxonomy.split('|')
    return str(temp[0])

# Process each line, extract ReadName/ReadID and Aligned/Mapped result
def convert_line_sta(line):
    tempLine = line.split('\t')
    res = ""
    if READTOKEN in tempLine[0]:
        res += tempLine[0] + " "
        if str(tempLine[2]) == "*":
            res += tempLine[2]
        else:
            res += extract_ID_S(str(tempLine[2]))
    return res

# Write extracted information std output
output = open('processed_BT_log', 'w')

# Execute line-processing and output
with open(BOWTLOG, buffering=2000000000) as f:
    for line in f:
        temp = []
        temp = convert_line_sta(line)
        if temp != "":
            output.write(str(temp)+'\n')
        #         j += 1
        # if j == 1000:
        #         break
