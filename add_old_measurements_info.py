import mariadb
import sys
import json
import csv
try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost",
        port=3306,
        database="eits"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
# Get Cursor
cur = conn.cursor()

# Get row ID from table Data
def add_data(ID, in_scope, testable):
    try: 
        #cur.execute("UPDATE Data SET in_scope = ?, testable = ? WHERE ID = ?", (in_scope,testable,ID)) 
        cur.execute("UPDATE Data SET in_scope = ?, testable = ? WHERE ID = ?", (in_scope,testable,ID))
    except mariadb.Error as e: 
        print(f"Error adding data to MariaDB: {e}")
    conn.commit() 

# Open JSON from file
with open('2021.json') as f:
    data = json.load(f)
for i in range(0,len(data)):
    add_data(data[i]['ref_idx'], data[i]['in_scope'], data[i]['testable'])
