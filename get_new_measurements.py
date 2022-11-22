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
cur.execute("SELECT ID FROM Data")
id_2022_temp = []
id_2021 = []
id_2022_temp = cur.fetchall()

# Open JSON from file
with open('2021.json') as f:
    data = json.load(f)
for i in range(0,len(data)):
    id_2021.append(data[i]['ref_idx'])


id_2021_set = set(id_2021)
id_2022 = []
for row in id_2022_temp:
    id_2022.append(row[0])
id_2022_set = set(id_2022)
new_measurements_set = id_2022_set - id_2021_set
new_measurements = list(new_measurements_set)
new_measurements.sort()
print(new_measurements)
with open('new_measurements.csv', 'w') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(new_measurements)