import sqlite3

ARTHEAD='head_0507.txt' # data source
sqlite_file = 'Alignment.sqlite'    # name of the sqlite database file
table_name = 'ARTMOCK'  # name of the table to be created
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

# Strip redundant charactor, split strings into substrings and insert into database 
with open(ARTHEAD, buffering=2000000000) as f:
    for line in f:
        processed = str(line).strip('>')
        tempSplit = processed.split('\t')
        sectionID = str(tempSplit[0])
        fullTax = str(tempSplit[1]).split(';')

        c.execute("INSERT INTO {tn} ({c1}, {c2}, {c3}, {c4}, {c5}, {c6}, {c7}, {c8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"\
            .format(tn=table_name, c1=column_1, c2=column_2, c3=column_3, c4=column_4, c5=column_5, c6=column_6, c7=column_7, c8=column_8),\
             (sectionID, str(fullTax[0]), str(fullTax[1]), str(fullTax[2]), str(fullTax[3]), str(fullTax[4]), str(fullTax[5]),\
              str(fullTax[6])))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()