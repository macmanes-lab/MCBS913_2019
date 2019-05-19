KLLOG='../../mock_comm_even_sam/mock_comm_even.sam'


#READTOKEN = "ERR"

def convert_line_sta(line):
	tempLine = line.split('\t')
	res = ""
	res += tempLine[0] + " "
	res += tempLine[2]
	return res

output = open('kl_even.txt','w')
with open(KLLOG, buffering=2000000000) as f:
    for line in f:
        temp = []
        temp = convert_line_sta(line)
        if temp != "":
                output.write(str(temp)+'\n')