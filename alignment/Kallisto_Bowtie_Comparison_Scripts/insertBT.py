import sqlite3

sqlite_file = 'Alignment.sqlite'    # name of the sqlite database file
table_name_1 = 'BT'  # name of the table to be created
new_column_1 = 'ReferenceName' # name of the column_1 - Read_Name
new_column_2 = 'MappingResult' # name of the column_2 - Alignment_Result
data_set = 'processed_BT_log' # data source

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

with open(data_set, buffering=2000000000) as f:
    for line in f:
        line =  line.strip('\n')
        tempLine = line.split(' ')
        c.execute("INSERT INTO {tn} ({rf}, {mrn}) VALUES (?, ?)"\
            .format(tn=table_name_1, rf=new_column_1, mrn=new_column_2), (str(tempLine[0]), str(tempLine[1])))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()