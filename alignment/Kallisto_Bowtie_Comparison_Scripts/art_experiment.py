import sqlite3

sqlite_file = 'Alignment.sqlite'    # name of the sqlite database file
table_name_MOCK = 'ARTMOCK' # name of the table --- standard
table_name_B = 'ARTB'  # name of the table --- Bowtie Art Sam
table_name_K = 'ARTK'  # name of the table --- Kallisto Art Sam
column_1 = 'section_id' # name of the column_1 - section_id
column_2 = 'kingdom' # name of the column_2 - kingdome
column_3 = 'phylum'  # name of the cloumn_3 - phylum
column_4 = 'class' # name of the cloumn_4 - class
column_5 = 'orders' # name of the cloumn_5 - orders
column_6 = 'family' # name of the cloumn_6 - family
column_7 = 'genus' # name of the cloumn_7 - genus
column_8 = 'species' # name of the cloumn_8 - species

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

print("=================Kallisto Statistics=================")

# Total reads in Kallisto
c.execute("SELECT COUNT(*) FROM {tb};".format(tb=table_name_K))
KL_OverAll_Result = c.fetchone()[0]
print("Kallisto art overall reads: " + str(KL_OverAll_Result))

# Full ranking lineage result in Kallisto
c.execute("SELECT COUNT(*) FROM {tb} WHERE {c3} <> '*';".format(tb=table_name_K, c3=column_3))
KL_Full_R_Result = c.fetchone()[0]
print("Kallisto full mapped ranking lineage reads: " + str(KL_Full_R_Result))

# Partial ranking lineage result in Kallisto
c.execute("SELECT COUNT(*) FROM {tb} WHERE {c2} <> '*' AND {c3} == '*';".format(tb=table_name_K, c2=column_2, c3=column_3))
KL_Partial_R_Result = c.fetchone()[0]
print("Kallisto partial mapped ranking lineage reads: " + str(KL_Partial_R_Result))

# Unmapped result in Kallisto
c.execute("SELECT COUNT(*) FROM {tb} WHERE {c2} == '*';".format(tb=table_name_K, c2=column_2))
KL_unmapped_Result = c.fetchone()[0]
print("Kallisto art unmapped reads: " + str(KL_unmapped_Result))

res = "{0:.2f}%".format((float(KL_unmapped_Result) / float(KL_OverAll_Result)) * 100)
print("Kallisto art mapped rate: " + str("{0:.2f}%".format((1 - (float(KL_unmapped_Result) / float(KL_OverAll_Result))) * 100)))
print("Kallisto art unmapped rate: " + str(res))

print("\n=================Kallisto Lineage Accuracy=================")

# kingdom level accuracy in Kallisto
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c2} == 'Bacteria';".format(tb=table_name_K, c2=column_2))
KL_kingdom = float(c.fetchone()[0])
temp = float(KL_Full_R_Result) + float(KL_Partial_R_Result)
res = "{0:.2f}%".format((KL_kingdom / temp) * 100)
print("Kallisto kingdom-level accuracy is " + str(res))

# phylum level accuracy in Kallisto
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c3} IN (SELECT {c3} FROM {mtb});".format(tb=table_name_K, c3=column_3, mtb=table_name_MOCK))
KL_phylum = float(c.fetchone()[0])
temp = float(KL_Full_R_Result) + float(KL_Partial_R_Result)
res = "{0:.2f}%".format((KL_phylum / temp) * 100)
print("Kallisto phylum-level accuracy is " + str(res))

# class level accuracy in Kallisto
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c4} IN (SELECT {c4} FROM {mtb});".format(tb=table_name_K, c4=column_4, mtb=table_name_MOCK))
KL_class = float(c.fetchone()[0])
temp = float(KL_Full_R_Result) + float(KL_Partial_R_Result)
res = "{0:.2f}%".format((KL_class / temp) * 100)
print("Kallisto class-level accuracy is " + str(res))

# orders accuracy in Kallisto
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c5} IN (SELECT {c5} FROM {mtb}) OR {c5} == 'Enterobacteriales';".format(tb=table_name_K, c5=column_5, mtb=table_name_MOCK))
KL_orders = float(c.fetchone()[0])
temp = float(KL_Full_R_Result) + float(KL_Partial_R_Result)
res = "{0:.2f}%".format((KL_orders / temp) * 100)
print("Kallisto orders-level accuracy is " + str(res))

# family orders accuracy in Kallisto
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c6} IN (SELECT {c6} FROM {mtb});".format(tb=table_name_K, c6=column_6, mtb=table_name_MOCK))
KL_family = float(c.fetchone()[0])
temp = float(KL_Full_R_Result) + float(KL_Partial_R_Result)
res = "{0:.2f}%".format((KL_family / temp) * 100)
print("Kallisto family-level accuracy is " + str(res))

# genus orders accuracy in Kallisto
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c7} IN (SELECT {c7} FROM {mtb});".format(tb=table_name_K, c7=column_7, mtb=table_name_MOCK))
KL_genus = float(c.fetchone()[0])
temp = float(KL_Full_R_Result) + float(KL_Partial_R_Result)
res = "{0:.2f}%".format((KL_genus / temp) * 100)
print("Kallisto genus-level accuracy is " + str(res))

# species orders accuracy in Kallisto
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c8} IN (SELECT {c8} FROM {mtb});".format(tb=table_name_K, c8=column_8, mtb=table_name_MOCK))
KL_species = float(c.fetchone()[0])
temp = float(KL_Full_R_Result) + float(KL_Partial_R_Result)
res = "{0:.2f}%".format((KL_species / temp) * 100)
print("Kallisto species-level accuracy is " + str(res))

print("\n=================Bowtie Statistics=================")

# Total reads in Bowtie
c.execute("SELECT COUNT(*) FROM {tb};".format(tb=table_name_B))
BT_OverAll_Result = c.fetchone()[0]
print("Bowtie art overall reads: " + str(BT_OverAll_Result))

# Full ranking lineage result in Bowtie
c.execute("SELECT COUNT(*) FROM {tb} WHERE {c3} <> '*';".format(tb=table_name_B, c3=column_3))
BT_Full_R_Result = c.fetchone()[0]
print("Bowtie full ranking lineage reads: " + str(BT_Full_R_Result))

# Partial ranking lineage result in Bowtie
c.execute("SELECT COUNT(*) FROM {tb} WHERE {c2} <> '*' AND {c3} == '*';".format(tb=table_name_B, c2=column_2, c3=column_3))
BT_Partial_R_Result = c.fetchone()[0]
print("Bowtie partial ranking lineage reads: " + str(BT_Partial_R_Result))

# Unmapped result in Bowtie
c.execute("SELECT COUNT(*) FROM {tb} WHERE {c2} == '*';".format(tb=table_name_B, c2=column_2))
BT_unmapped_Result = c.fetchone()[0]
print("Bowtie unmapped reads: " + str(BT_unmapped_Result))

res = "{0:.2f}%".format((float(BT_unmapped_Result) / float(BT_OverAll_Result)) * 100)
print("Bowtie art mapped rate: " + str("{0:.2f}%".format((1 - (float(BT_unmapped_Result) / float(BT_OverAll_Result))) * 100)))
print("Bowtie art unmapped rate: " + str(res))

print("\n=================Bowtie Lineage Accuracy=================")

# kingdom level accuracy in Bowtie
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c2} == 'Bacteria';".format(tb=table_name_B, c2=column_2))
BT_kingdom = float(c.fetchone()[0])
temp = float(BT_Full_R_Result) + float(BT_Partial_R_Result)
res = "{0:.2f}%".format((BT_kingdom / temp) * 100)
print("Bowtie kingdom-level accuracy is " + str(res))

# phylum level accuracy in Bowtie
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c3} IN (SELECT {c3} FROM {mtb});".format(tb=table_name_B, c3=column_3, mtb=table_name_MOCK))
BT_phylum = float(c.fetchone()[0])
temp = float(BT_Full_R_Result) + float(BT_Partial_R_Result)
res = "{0:.2f}%".format((BT_phylum / temp) * 100)
print("Bowtie phylum-level accuracy is " + str(res))

# class level accuracy in Bowtie
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c4} IN (SELECT {c4} FROM {mtb});".format(tb=table_name_B, c4=column_4, mtb=table_name_MOCK))
BT_class = float(c.fetchone()[0])
temp = float(BT_Full_R_Result) + float(BT_Partial_R_Result)
res = "{0:.2f}%".format((BT_class / temp) * 100)
print("Bowtie class-level accuracy is " + str(res))

# orders accuracy in Bowtie
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c5} IN (SELECT {c5} FROM {mtb}) OR {c5} == 'Enterobacteriales';".format(tb=table_name_B, c5=column_5, mtb=table_name_MOCK))
BT_orders = float(c.fetchone()[0])
temp = float(BT_Full_R_Result) + float(BT_Partial_R_Result)
res = "{0:.2f}%".format((BT_orders / temp) * 100)
print("Bowtie orders-level accuracy is " + str(res))

# family orders accuracy in Bowtie
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c6} IN (SELECT {c6} FROM {mtb});".format(tb=table_name_B, c6=column_6, mtb=table_name_MOCK))
BT_family = float(c.fetchone()[0])
temp = float(BT_Full_R_Result) + float(BT_Partial_R_Result)
res = "{0:.2f}%".format((BT_family / temp) * 100)
print("Bowtie family-level accuracy is " + str(res))

# genus orders accuracy in Bowtie
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c7} IN (SELECT {c7} FROM {mtb});".format(tb=table_name_B, c7=column_7, mtb=table_name_MOCK))
BT_genus = float(c.fetchone()[0])
temp = float(BT_Full_R_Result) + float(BT_Partial_R_Result)
res = "{0:.2f}%".format((BT_genus / temp) * 100)
print("Bowtie genus-level accuracy is " + str(res))

# species orders accuracy in Bowtie
c.execute("SELECT COUNT(*) FROM {tb} \
    WHERE {c8} IN (SELECT {c8} FROM {mtb});".format(tb=table_name_B, c8=column_8, mtb=table_name_MOCK))
BT_species = float(c.fetchone()[0])
temp = float(BT_Full_R_Result) + float(BT_Partial_R_Result)
res = "{0:.2f}%".format((BT_species / temp) * 100)
print("Bowtie species-level accuracy is " + str(res))

# error verification
# c.execute("SELECT COUNT(*) FROM {tb} WHERE section_id NOT LIKE '%NC%';".format(tb=table_name_B))
# BT_ERROR = c.fetchone()[0]
# print("Bowtie art ERROR reads: " + str(BT_ERROR))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()