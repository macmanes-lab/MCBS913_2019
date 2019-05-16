import sqlite3

sqlite_file = 'Alignment.sqlite'    # name of the sqlite database file
# table_name_1 = 'KEVEN'  # name of the table to be created
# table_name_2 = 'BEVEN'  # name of the table to be created
# new_field_1 = 'ReferenceName' # name of the column_2
# new_column_2 = 'MappingResult' # name of the column_3
# field_type = 'TEXT'  # column data type
# column_type = 'TEXT'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

## Create a new SQLite table with 1 column for Bowtie and Kallisto log and even
# c.execute('CREATE TABLE {tn} ({nf} {ft})'\
#         .format(tn=table_name_1, nf=new_field_1, ft=field_type))

# c.execute('CREATE TABLE {tn} ({nf} {ft})'\
#         .format(tn=table_name_2, nf=new_field_1, ft=field_type))

# Create new tables for art comparison
c.execute('CREATE TABLE ARTB (section_id TEXT,kingdom TEXT,phylum TEXT,class TEXT,orders TEXT,family TEXT,genus TEXT,species TEXT)')
c.execute('CREATE TABLE ARTK (section_id TEXT,kingdom TEXT,phylum TEXT,class TEXT,orders TEXT,family TEXT,genus TEXT,species TEXT)')

## Update table with adding a new column
# c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
#         .format(tn=table_name_1, cn=new_column_2, ct=column_type))

# c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
#         .format(tn=table_name_2, cn=new_column_2, ct=column_type))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
