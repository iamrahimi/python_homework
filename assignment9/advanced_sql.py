import sqlite3


# Connect to the database

with sqlite3.connect("./db/lesson.db") as conn:
    # Query 1: Products in first 5 orders
    print("First 5 orders and their products:\n")
    query1 = """
    SELECT o.order_id, li.line_item_id, p.product_name
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    WHERE o.order_id IN (
        SELECT order_id
        FROM orders
        ORDER BY order_id
        LIMIT 5
    )
    ORDER BY o.order_id, li.line_item_id;
    """
    cursor1 = conn.execute(query1)
    for row in cursor1.fetchall():
        print(f"Order ID: {row[0]}, Line Item ID: {row[1]}, Product: {row[2]}")

    print("\nTotal price for first 5 orders:\n")
    # Query 2: Total price per order
    query2 = """
    SELECT o.order_id, SUM(p.price * li.quantity) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5;
    """
    cursor2 = conn.execute(query2)
    for row in cursor2.fetchall():
        print(f"Order ID: {row[0]}, Total Price: ${row[1]:.2f}")

    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    try:
        # Start transaction
        print("\nCreating a new order for Perez and Sons...")

        # Get customer_id
        cursor.execute("SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'")
        customer_id = cursor.fetchone()[0]

        # Get employee_id
        cursor.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name ='Harris'")
        employee_id = cursor.fetchone()[0]

        # Get product_ids of 5 least expensive products
        cursor.execute("SELECT product_id FROM products ORDER BY price LIMIT 5")
        product_ids = [row[0] for row in cursor.fetchall()]

        # Insert order and get order_id
        cursor.execute("""
            INSERT INTO orders (customer_id, employee_id)
            VALUES (?, ?)
            RETURNING order_id;
        """, (customer_id, employee_id))
        order_id = cursor.fetchone()[0]

        # Insert line_items (10 units of each product)
        for product_id in product_ids:
            cursor.execute("""
                INSERT INTO line_items (order_id, product_id, quantity)
                VALUES (?, ?, ?);
            """, (order_id, product_id, 10))

        # Commit the transaction
        conn.commit()

        print(f"Order {order_id} created with 5 line items.")

        # Retrieve and print the new line items
        print("\nLine items in the new order:\n")
        cursor.execute("""
            SELECT li.line_item_id, li.quantity, p.product_name
            FROM line_items li
            JOIN products p ON li.product_id = p.product_id
            WHERE li.order_id = ?;
        """, (order_id,))
        rows = cursor.fetchall()
        for row in rows:
            print(f"Line Item ID: {row[0]}, Quantity: {row[1]}, Product: {row[2]}")

    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")

    try: 

        cursor3 = conn.cursor()

        query3 = """
                SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) AS order_count
                FROM employees e
                JOIN orders o ON e.employee_id = o.employee_id
                GROUP BY e.employee_id
                HAVING COUNT(o.order_id) > 5;
            """

        cursor3.execute(query3)
        results = cursor3.fetchall()

        print("Employees with more than 5 orders:")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Orders: {row[3]}")
    except Exception as e:
        print(f"Query failed: {e}")