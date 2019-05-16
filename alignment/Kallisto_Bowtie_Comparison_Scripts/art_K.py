import sqlite3

ARTSAM='art_KL.sam' # art.sam outputed by Kallisto
sqlite_file = 'Alignment.sqlite'    # name of the sqlite database file
table_name = 'ARTK'  # name of the table to be created
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

# Method to extract first 2 substrings from full species result
def discardSub(input):
    res = ""
    tokens = input.split('_')
    if len(tokens) > 1 :
        res += tokens[0]
        res += '_'
        res += tokens[1]
    else :
        res = str(input)
    return res

# Default value for unmapped result and partial mapped result
unmapped_res = '*'

# line processing and database insertion
with open(ARTSAM, buffering=2000000000) as f:
    for line in f:
        tempSplit = str(line).split('\t')
        fullSectionID = str(tempSplit[0]).split('-')
        sectionID = fullSectionID[0]
        if str(tempSplit[2]) != '*':
            fullTax = str(tempSplit[2]).split('|')
            subs = str(fullTax[1]).split(';')

            # full mapped result - 1: length 6 can be fixed
            if len(subs) == 6:
                c.execute("INSERT INTO {tn} ({c1}, {c2}, {c3}, {c4}, {c5}, {c6}, {c7}, {c8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"\
                .format(tn=table_name, c1=column_1, c2=column_2, c3=column_3, c4=column_4, c5=column_5, c6=column_6, c7=column_7, c8=column_8),\
                (sectionID, str(subs[0]), str(subs[1]), str(subs[2]), str(subs[3]), str(subs[4]), str(subs[4]), discardSub(subs[5])))

            # full mapped results -2
            elif len(subs) > 6:
                c.execute("INSERT INTO {tn} ({c1}, {c2}, {c3}, {c4}, {c5}, {c6}, {c7}, {c8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"\
                .format(tn=table_name, c1=column_1, c2=column_2, c3=column_3, c4=column_4, c5=column_5, c6=column_6, c7=column_7, c8=column_8),\
                (sectionID, str(subs[0]), str(subs[1]), str(subs[2]), str(subs[3]), str(subs[4]), str(subs[5]), discardSub(subs[6])))

            # partial mapped results: discard everything BUT kingdom(first sub string) and species(last substring)
            else :
                c.execute("INSERT INTO {tn} ({c1}, {c2}, {c3}, {c4}, {c5}, {c6}, {c7}, {c8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"\
                .format(tn=table_name, c1=column_1, c2=column_2, c3=column_3, c4=column_4, c5=column_5, c6=column_6, c7=column_7, c8=column_8),\
                (sectionID, str(subs[0]), unmapped_res, unmapped_res, unmapped_res, unmapped_res, unmapped_res, discardSub(subs[len(subs) - 1])))
        
        # Unmapped result
        else :
            c.execute("INSERT INTO {tn} ({c1}, {c2}, {c3}, {c4}, {c5}, {c6}, {c7}, {c8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"\
            .format(tn=table_name, c1=column_1, c2=column_2, c3=column_3, c4=column_4, c5=column_5, c6=column_6, c7=column_7, c8=column_8),\
            (sectionID, unmapped_res, unmapped_res, unmapped_res, unmapped_res, unmapped_res, unmapped_res, unmapped_res))


# Committing changes and closing the connection to the database file
conn.commit()
conn.close()