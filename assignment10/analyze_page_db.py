import sqlite3
import pandas as pd
import os

# Paths
db_path = 'db/page.db'
summary_file = 'assignment10/assignment10.txt'

# Connect to DB
conn = sqlite3.connect(db_path)

# Load data into DataFrame
df = pd.read_sql_query("SELECT * FROM page_data", conn)
conn.close()

# Count headers and links (assuming 'type' column has these values)
num_headers = df[df['type'].str.lower() == 'header'].shape[0]
num_links = df[df['type'].str.lower() == 'link'].shape[0]

# Find most frequent type of data
most_freq_type = df['type'].value_counts().idxmax()
most_freq_count = df['type'].value_counts().max()

# Create summary text
summary = (
    f"Analysis of scraped data from SQLite database:\n"
    f"- Number of headers: {num_headers}\n"
    f"- Number of links: {num_links}\n"
    f"- Most frequent data type: '{most_freq_type}' with {most_freq_count} occurrences.\n"
)

# Write summary to file
with open(summary_file, 'w') as f:
    f.write(summary)

print("Summary written to", summary_file)