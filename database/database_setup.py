import sqlite3
import os

# ✅ Ensure database folder exists
os.makedirs('database', exist_ok=True)

# ✅ Create or connect to the database
conn = sqlite3.connect('database/peers.db')
c = conn.cursor()

# ✅ Create table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    interests TEXT
)
''')

# ✅ Add sample users
sample_data = [
    ('Radhika', 'radhika@gmail.com', 'AI,ML,Python'),
    ('Aarav', 'aarav@gmail.com', 'Data Science,ML,Python'),
    ('Diya', 'diya@gmail.com', 'Web,JavaScript,HTML,CSS'),
    ('Vikram', 'vikram@gmail.com', 'AI,DL,Python'),
    ('Neha', 'neha@gmail.com', 'Web,React,JS')
]

c.executemany('INSERT OR IGNORE INTO users (name, email, interests) VALUES (?, ?, ?)', sample_data)
conn.commit()
conn.close()

print("✅ Database and sample users created successfully!")
