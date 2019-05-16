import sqlite3

sqlite_file = 'Alignment.sqlite' # name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

print("======================EVEN======================\n")

# overall reads in Bowtie
c.execute("SELECT COUNT(*) FROM BEVEN;")
BT_OverAll_Result = c.fetchone()[0]
print("Bowtie overall reads: " + str(BT_OverAll_Result))

# found mapped result number in Bowtie
c.execute("SELECT COUNT(*) FROM BEVEN WHERE MappingResult NOT LIKE '%*%';")
BT_M_Result = c.fetchone()[0]
align_rate_B = "{0:.2f}%".format((float(BT_M_Result) / float(BT_OverAll_Result)) * 100)
print("Bowtie algined reads: " + str(BT_M_Result))
print("Bowtie aligned rate: " + str(align_rate_B))

# overall reads in Bowtie
c.execute("SELECT COUNT(*) FROM KEVEN;")
KL_OverAll = c.fetchone()[0]
print("Kallisto overall reads: " + str(KL_OverAll))

# found mapped result number in Kallisto
c.execute("SELECT COUNT(*) FROM KEVEN WHERE MappingResult NOT LIKE '%*%';")
KL_M_Result = c.fetchone()[0]
align_rate_K = "{0:.2f}%".format((float(KL_M_Result) / float(KL_OverAll)) * 100)
print("Kallisto algined results: " + str(KL_M_Result))
print("Kallisto aligned rate: " + str(align_rate_K))

# Overlap of Bowtie and Kallisto
c.execute("""SELECT COUNT(*) FROM KEVEN \
    JOIN BEVEN ON KEVEN.ReferenceName = BEVEN.ReferenceName \
    WHERE KEVEN.MappingResult = BEVEN.MappingResult \
        AND KEVEN.MappingResult NOT LIKE '%*%' ;""")
Overlap_Result = c.fetchone()[0]
print("Overlapping aligned results: " + str(Overlap_Result))
# percent of Bowtie aligned result shared with KL 
temp_1 = "{0:.2f}%".format((float(Overlap_Result) / float(KL_M_Result)) * 100)
print("The percentage of Kallisto aligned results that are shared with Bowtie is " + str(temp_1))
# percent of KL aligned result shared with Bowtie 
temp_2 = "{0:.2f}%".format((float(Overlap_Result) / float(BT_M_Result)) * 100)
print("The percent of Bowtie aligned results that are shared with Kallisto is " + str(temp_2))

# Read solely processed by KL (missed reads in BT)
c.execute("SELECT COUNT(*) FROM KEVEN \
    LEFT JOIN BEVEN \
    ON KEVEN.ReferenceName = BEVEN.ReferenceName \
    WHERE BEVEN.ReferenceName IS NULL;")
KL_SOLE_Result = c.fetchone()[0]
print("Missing reads in Bowtie: " + str(KL_SOLE_Result))

# Read solely processed by BT (missed reads in KL)
c.execute("SELECT COUNT(*) FROM BEVEN \
    LEFT JOIN KEVEN \
    ON KEVEN.ReferenceName = BEVEN.ReferenceName \
    WHERE KEVEN.ReferenceName IS NULL;")
KL_SOLE_Result = c.fetchone()[0]
print("Missing reads in Kallisto: " + str(KL_SOLE_Result))

# Read soley aligned in BT
c.execute("SELECT COUNT(*) FROM BEVEN \
    LEFT JOIN KEVEN \
    ON BEVEN.ReferenceName = KEVEN.ReferenceName \
    WHERE BEVEN.MappingResult NOT LIKE '%*%' AND KEVEN.MappingResult LIKE '%*%';")
BT_SOLE_Result = c.fetchone()[0]
print("Soley aligned reads in Bowtie: " + str(BT_SOLE_Result))

# Read soley aligned in KL
c.execute("SELECT COUNT(*) FROM KEVEN \
    LEFT JOIN BEVEN \
    ON KEVEN.ReferenceName = BEVEN.ReferenceName \
    WHERE KEVEN.MappingResult NOT LIKE '%*%' AND BEVEN.MappingResult LIKE '%*%';")
KL_SOLE_Result = c.fetchone()[0]
print("Soley aligned reads in Kallisto: " + str(KL_SOLE_Result))

# Count Multiple Mapping in KL
# c.execute("SELECT ReferenceName, COUNT(*) \
#     FROM KEVEN \
#     GROUP BY ReferenceName \
#     HAVING (COUNT(*) > 1);")
# KL_DUP_Result = c.fetchall()
# length = len(KL_DUP_Result)
# print("Multiple mapping reads in Kallisto: " + str(length))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
