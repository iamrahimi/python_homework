import sqlite3
import pandas as pd
import os

# Define the path to the database
db_path = "db/lesson.db"

# Connect to the database
with sqlite3.connect(db_path) as conn:
    # Read data from JOIN into a DataFrame
    query = """
    SELECT
        line_items.line_item_id,
        line_items.quantity,
        line_items.product_id,
        products.product_name,
        products.price
    FROM line_items
    JOIN products ON line_items.product_id = products.product_id
    """
    df = pd.read_sql_query(query, conn)

# Print first 5 rows to confirm data
print("Initial DataFrame:")
print(df.head())

# Add 'total' column: quantity * price
df['total'] = df['quantity'] * df['price']

# Print again to confirm new column
print("\nDataFrame with 'total' column:")
print(df.head())

# Group by product_id and aggregate
summary_df = df.groupby('product_id').agg(
    line_item_count=('line_item_id', 'count'),
    total_sales=('total', 'sum'),
    product_name=('product_name', 'first')
).reset_index()

# Sort by product_name
summary_df = summary_df.sort_values(by='product_name')

# Print final summary
print("\nSummary DataFrame:")
print(summary_df.head())

# Write to CSV in assignment7 folder
output_path = os.path.join(os.getcwd(), "assignment7/order_summary.csv")
summary_df.to_csv(output_path, index=False)
print(f"\nSummary written to: {output_path}")