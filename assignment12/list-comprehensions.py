import pandas as pd

# Load CSV data into a DataFrame
df = pd.read_csv('csv/employees.csv')

# Create a list of full names using list comprehension
full_names = [f"{row['first_name']} {row['last_name']}" for _, row in df.iterrows()]
print("All Names:")
print(full_names)

# Create a filtered list with names containing the letter 'e'
names_with_e = [name for name in full_names if 'e' in name.lower()]
print("\nNames Containing 'e':")
print(names_with_e)