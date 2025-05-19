import sqlite3
import csv
import os


csv_file_path = 'assignment10/page.csv'
db_path = 'db/page.db'

# Connect to SQLite DB (creates if not exists)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS page_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    content TEXT,
    extra TEXT
)
''')

# Clear table if you want to re-run script multiple times (optional)
cursor.execute('DELETE FROM page_data')

# Read CSV and insert into DB
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('''
            INSERT INTO page_data (type, content, extra)
            VALUES (?, ?, ?)
        ''', (row['type'], row['content'], row['extra']))

conn.commit()

# Retrieve and print data
cursor.execute('SELECT * FROM page_data')
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()