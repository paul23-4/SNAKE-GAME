import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('snake_game.db')
cursor = conn.cursor()

# Execute query to fetch all records from the users table
cursor.execute('SELECT * FROM users')

# Fetch all the records
rows = cursor.fetchall()

# Print the fetched records
for row in rows:
    print(row)

# Close the database connection
conn.close()
