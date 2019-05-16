import sqlite3

sqlite_file = 'Alignment.sqlite' # name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

print("======================LOG======================\n")

# overall reads in Bowtie
c.execute("SELECT COUNT(*) FROM BT;")
BT_OverAll_Result = c.fetchone()[0]
print("Bowtie overall reads: " + str(BT_OverAll_Result))

# found mapped result number in Bowtie
c.execute("SELECT COUNT(*) FROM BT WHERE MappingResult NOT LIKE '%*%';")
BT_M_Result = c.fetchone()[0]
align_rate_B = "{0:.2f}%".format((float(BT_M_Result) / float(BT_OverAll_Result)) * 100)
print("Bowtie algined reads: " + str(BT_M_Result))
print("Bowtie aligned rate: " + str(align_rate_B))

# overall reads in Bowtie
c.execute("SELECT COUNT(*) FROM KL;")
KL_OverAll = c.fetchone()[0]
print("Kallisto overall reads: " + str(KL_OverAll))

# found mapped result number in Kallisto
c.execute("SELECT COUNT(*) FROM KL WHERE MappingResult NOT LIKE '%*%';")
KL_M_Result = c.fetchone()[0]
align_rate_K = "{0:.2f}%".format((float(KL_M_Result) / float(KL_OverAll)) * 100)
print("Kallisto algined results: " + str(KL_M_Result))
print("Kallisto aligned rate: " + str(align_rate_K))

# Overlap of Bowtie and Kallisto
c.execute("""SELECT COUNT(*) FROM KL \
    JOIN BT ON KL.ReferenceName = BT.ReferenceName \
    WHERE KL.ReferenceName = BT.ReferenceName AND KL.MappingResult = BT.MappingResult AND KL.MappingResult NOT LIKE '%*%' ;""")
Overlap_Result = c.fetchone()[0]
print("Overlapping aligned results: " + str(Overlap_Result))
# percent of Bowtie aligned result shared with KL 
temp_1 = "{0:.2f}%".format((float(Overlap_Result) / float(KL_M_Result)) * 100)
print("The percentage of Kallisto aligned results that are shared with Bowtie is " + str(temp_1))
# percent of KL aligned result shared with Bowtie 
temp_2 = "{0:.2f}%".format((float(Overlap_Result) / float(BT_M_Result)) * 100)
print("The percent of Bowtie aligned results that are shared with Kallisto is " + str(temp_2))

# Read solely processed by KL (missed reads in BT)
c.execute("SELECT COUNT(*) FROM KL \
    LEFT JOIN BT \
    ON KL.ReferenceName = BT.ReferenceName \
    WHERE BT.ReferenceName IS NULL;")
KL_SOLE_Result = c.fetchone()[0]
print("Missing reads in Bowtie: " + str(KL_SOLE_Result))

# Read solely processed by BT (missed reads in KL)
c.execute("SELECT COUNT(*) FROM BT \
    LEFT JOIN KL \
    ON KL.ReferenceName = BT.ReferenceName \
    WHERE KL.ReferenceName IS NULL;")
KL_SOLE_Result = c.fetchone()[0]
print("Missing reads in Kallisto: " + str(KL_SOLE_Result))

# Read soley aligned in BT
c.execute("SELECT COUNT(*) FROM BT \
    LEFT JOIN KL \
    ON BT.ReferenceName = KL.ReferenceName \
    WHERE BT.MappingResult NOT LIKE '%*%' AND KL.MappingResult LIKE '%*%';")
BT_SOLE_Result = c.fetchone()[0]
print("Soley aligned reads in Bowtie: " + str(BT_SOLE_Result))

# Read soley aligned in KL
c.execute("SELECT COUNT(*) FROM KL \
    LEFT JOIN BT \
    ON KL.ReferenceName = BT.ReferenceName \
    WHERE KL.MappingResult NOT LIKE '%*%' AND BT.MappingResult LIKE '%*%';")
KL_SOLE_Result = c.fetchone()[0]
print("Soley aligned reads in Kallisto: " + str(KL_SOLE_Result))

# Count Multiple Mapping in KL
# c.execute("SELECT ReferenceName, COUNT(*) \
#     FROM KL \
#     GROUP BY ReferenceName \
#     HAVING (COUNT(*) > 1);")
# KL_DUP_Result = c.fetchall()
# length = len(KL_DUP_Result)
# print("Multiple mapping reads in Kallisto: " + str(length))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
