import sqlite3

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS publishers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        );
    """)


def add_publisher(conn, name):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO publishers (name) VALUES (?)", (name,))
    except Exception as e:
        print(f"Error adding publisher '{name}': {e}")

def add_magazine(conn, name, publisher_name):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM publishers WHERE name = ?", (publisher_name,))
        publisher = cursor.fetchone()
        if publisher:
            cursor.execute("INSERT OR IGNORE INTO magazines (name, publisher_id) VALUES (?, ?)", (name, publisher[0]))
        else:
            print(f"Publisher '{publisher_name}' not found for magazine '{name}'")
    except Exception as e:
        print(f"Error adding magazine '{name}': {e}")

def add_subscriber(conn, name, address):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM subscribers WHERE name = ? AND address = ?
        """, (name, address))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", (name, address))
    except Exception as e:
        print(f"Error adding subscriber '{name}': {e}")

def add_subscription(conn, subscriber_name, subscriber_address, magazine_name, expiration_date):
    try:
        cursor = conn.cursor()

        # Get subscriber ID
        cursor.execute("""
            SELECT id FROM subscribers WHERE name = ? AND address = ?
        """, (subscriber_name, subscriber_address))
        subscriber = cursor.fetchone()

        # Get magazine ID
        cursor.execute("SELECT id FROM magazines WHERE name = ?", (magazine_name,))
        magazine = cursor.fetchone()

        if subscriber and magazine:
            cursor.execute("""
                SELECT id FROM subscriptions
                WHERE subscriber_id = ? AND magazine_id = ?
            """, (subscriber[0], magazine[0]))

            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date)
                    VALUES (?, ?, ?)
                """, (subscriber[0], magazine[0], expiration_date))
        else:
            print(f"Subscription could not be created: missing subscriber or magazine.")
    except Exception as e:
        print(f"Error adding subscription: {e}")


try:
    with sqlite3.connect("db/magazines.db") as conn:
        print("Database connected successfully!")
        conn.execute("PRAGMA foreign_keys = 1")

        cursor = conn.cursor()

        create_tables(conn)

        # Add publishers
        add_publisher(conn, "Oxford Media")
        add_publisher(conn, "Global Press")
        add_publisher(conn, "Bright Future Publishing")

        # Add magazines
        add_magazine(conn, "Tech Weekly", "Oxford Media")
        add_magazine(conn, "Health Digest", "Global Press")
        add_magazine(conn, "Nature Now", "Bright Future Publishing")

        # Add subscribers
        add_subscriber(conn, "Alice Johnson", "123 Main St")
        add_subscriber(conn, "Bob Smith", "456 Maple Ave")
        add_subscriber(conn, "Alice Johnson", "789 Elm Rd")  # Same name, different address

        # Add subscriptions
        add_subscription(conn, "Alice Johnson", "123 Main St", "Tech Weekly", "2025-12-01")
        add_subscription(conn, "Alice Johnson", "789 Elm Rd", "Nature Now", "2026-01-15")
        add_subscription(conn, "Bob Smith", "456 Maple Ave", "Health Digest", "2025-08-10")

        conn.commit()

        print("\nAll subscribers:")
        cursor = conn.execute("SELECT * FROM subscribers")
        for row in cursor.fetchall():
            print(row)

        print("\nAll magazines (sorted by name):")
        cursor = conn.execute("SELECT * FROM magazines ORDER BY name ASC")
        for row in cursor.fetchall():
            print(row)

        print("\nMagazines published by 'Oxford Media':")
        cursor = conn.execute("""
            SELECT m.id, m.name, m.publisher_id
            FROM magazines m
            JOIN publishers p ON m.publisher_id = p.id
            WHERE p.name = ?
        """, ("Oxford Media",))
        for row in cursor.fetchall():
            print(row)

        print("Database populated successfully.")

        
except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"General error: {e}")


