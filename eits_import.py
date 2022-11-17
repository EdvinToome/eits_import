from bs4 import BeautifulSoup
import re
import sys
import mariadb
import json
import requests
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

def add_data(GroupID, ID, Name, Description):
    try: 
        cur.execute("INSERT INTO Data (GroupID,ID,Name,Description) VALUES (?, ?, ?, ?)", (GroupID, ID, Name, Description)) 
    except mariadb.Error as e: 
        print(f"Error adding data to MariaDB: {e}")
    conn.commit() 

try:
    r = requests.get('https://eits.ria.ee/api/1/article/2022/cd7ed320f3c5279eb710386a76c26a58')
except(requests.exceptions.RequestException) as e:
    print(f"Error getting data from EITS: {e}")
    sys.exit(1)
content = r.json()['content']
content = ''.join(content.splitlines())
content = content.replace('\t', ' ')


soup = BeautifulSoup(content, 'lxml')
pattern = re.compile('INF.1')
for child in soup.recursiveChildGenerator():
     if child.name == 'h2' and pattern.match(child.text):
        measure_name_split =  re.split('[ .]', child.text, 3)
        measure_name = measure_name_split[3]
        i = 0
        while True:
            if child.find_next_siblings()[i].name == 'p':               
                measure_description_split = child.find_next_siblings()[i].text.split('.', 1)
                measure_full_id = measure_name_split[0] + '.' + measure_name_split[1] + '.' + measure_name_split[2] + '.' + measure_description_split[0]
                measure_group_id = measure_name_split[0] + '.' + measure_name_split[1]
                measure_description = measure_description_split[1]
                add_data(measure_group_id, measure_full_id, measure_name, measure_description)   
                i += 1
            else:
                break

