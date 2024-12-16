import json
import mysql.connector

# Load JSON data from a file
with open('D:/Code/my_first/cah_cards_full.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Connect to MySQL
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'
)
cursor = conn.cursor()

# Create database and tables
cursor.execute("CREATE DATABASE IF NOT EXISTS cah_cards CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
cursor.execute("USE cah_cards")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS packs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS white_cards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        text TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        pack_id INT,
        FOREIGN KEY (pack_id) REFERENCES packs(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS black_cards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        text TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        pack_id INT,
        FOREIGN KEY (pack_id) REFERENCES packs(id)
    )
""")

# Insert data into MySQL
for pack in data:
    # Insert pack
    cursor.execute("INSERT INTO packs (name) VALUES (%s)", (pack['name'],))
    pack_id = cursor.lastrowid

    # Insert white cards
    for card in pack['white']:
        cursor.execute("INSERT INTO white_cards (text, pack_id) VALUES (%s, %s)", (card['text'], pack_id))

    # Insert black cards
    if 'black' in pack:
        for card in pack['black']:
            cursor.execute("INSERT INTO black_cards (text, pack_id) VALUES (%s, %s)", (card['text'], pack_id))

# Commit the transaction
conn.commit()

# Retrieve and print data from MySQL
print("Packs:")
cursor.execute("SELECT * FROM packs")
for (id, name) in cursor.fetchall():
    print(f"ID: {id}, Name: {name}")

print("\nWhite Cards:")
cursor.execute("SELECT * FROM white_cards")
for (id, text, pack_id) in cursor.fetchall():
    print(f"ID: {id}, Text: {text}, Pack ID: {pack_id}")

print("\nBlack Cards:")
cursor.execute("SELECT * FROM black_cards")
for (id, text, pack_id) in cursor.fetchall():
    print(f"ID: {id}, Text: {text}, Pack ID: {pack_id}")

# Close the connection
cursor.close()
conn.close()