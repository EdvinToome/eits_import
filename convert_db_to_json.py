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


cur.execute("SELECT * FROM Data")
rows = cur.fetchall()
json_data = []
for row in rows:
    json_data.append({
        'group_id': row[0],
        'id': row[1],
        'name': row[2],
        'description': row[3],
        'in_scope': row[4],
        'testable': row[5]
    })
with open('2022.json', 'w') as f:
    json.dump(json_data, f, ensure_ascii=False)