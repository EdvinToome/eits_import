from bs4 import BeautifulSoup
import re
import sys
import mariadb
import json
import requests

# Connect to MariaDB Platform

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

# Get IDs of EITS measurements

structure = requests.get('https://eits.ria.ee/api/1/article/2022')
articles_id = []
measure_short_id = []
articles_title = []
main_object = ((structure.json()[0]['child_objects'])[0]['child_objects'])[1]['child_objects']

for x in range(0,len(main_object)):
    for y in range(0,len(main_object[x]['child_objects'])):
        if((((main_object[x]['child_objects'])[y]['child_objects'])[0]['title']) == '1 Kirjeldus'):
            articles_id.append(((main_object[x]['child_objects'])[y]['child_objects'])[2]['id'])
            articles_title.append((main_object[x]['child_objects'])[y]['title'])
        else:
            for z in range(0,len((main_object[x]['child_objects'])[y]['child_objects'])):
                if(((((main_object[x]['child_objects'])[y]['child_objects'])[z]['child_objects'])[0]['title']) == '1 Kirjeldus'):
                    articles_id.append((((main_object[x]['child_objects'])[y]['child_objects'])[z]['child_objects'])[2]['id'])
                    articles_title.append(((main_object[x]['child_objects'])[y]['child_objects'])[z]['title'])
                else:
                    for a in range(0,len(((main_object[x]['child_objects'])[y]['child_objects'])[z]['child_objects'])):
                        articles_id.append(((((main_object[x]['child_objects'])[y]['child_objects'])[z]['child_objects'])[a]['child_objects'])[2]['id'])
                        articles_title.append((((main_object[x]['child_objects'])[y]['child_objects'])[z]['child_objects'])[a]['title'])

for article_title in articles_title:
    sep = ':'
    stripped = article_title.split(sep, 1)[0]
    measure_short_id.append(stripped)

# Add data to database

def add_data(GroupID, ID, Name, Description):
    try: 
        cur.execute("INSERT INTO Data (GroupID,ID,Name,Description) VALUES (?, ?, ?, ?)", (GroupID, ID, Name, Description)) 
    except mariadb.Error as e: 
        print(f"Error adding data to MariaDB: {e}")
    conn.commit() 

# Get data from EITS articles

k = 0
for article_id in articles_id:
    try:
        r = requests.get('https://eits.ria.ee/api/1/article/2022/'+str(article_id))
    except(requests.exceptions.ConnectionError) as e:
        print(f"Error getting data from EITS: {e}")
        sys.exit(1)
    content = r.json()['content']
    content = ''.join(content.splitlines())
    content = content.replace('\t', ' ')

    soup = BeautifulSoup(content, 'lxml')
    pattern = re.compile(measure_short_id[k])
    
    for child in soup.recursiveChildGenerator():
         if child.name == 'h2' and pattern.match(child.text):
            measure_name_split =  re.split('[ ]', child.text, 1)
            measure_name = measure_name_split[1]
            i = 0
            while True:
                if child.find_next_siblings()[i].name == 'p':               
                    measure_description_split = child.find_next_siblings()[i].text.split('.', 1)
                    measure_full_id = measure_name_split[0]  + '.' + measure_description_split[0]
                    measure_description = measure_description_split[1]
                    add_data(measure_short_id[k], measure_full_id, measure_name, measure_description)   
                    i += 1
                    if len(child.find_next_siblings()) == i:
                        break
                else:
                    break
    k += 1

