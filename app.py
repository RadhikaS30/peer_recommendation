from flask import Flask, render_template, request
import sqlite3, os

app = Flask(__name__)

# ✅ Define correct database path
DB_PATH = os.path.join("database", "peers.db")

# ✅ Ensure database folder exists
os.makedirs("database", exist_ok=True)

# ✅ Initialize database if not already created
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    interests TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 🏠 Home Page
@app.route('/')
def home():
    return render_template('index.html')

# ➕ Add User Page
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        interests = request.form['interests']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO users (name, email, interests) VALUES (?, ?, ?)', (name, email, interests))
        conn.commit()
        conn.close()

        return "✅ User added successfully! <br><a href='/'>Back to Home</a>"
    return render_template('add_user.html')

# 💡 Recommendation Route
@app.route('/recommend', methods=['POST'])
def recommend():
    email = request.form['email']

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('SELECT interests FROM users WHERE email = ?', (email,))
    user_data = c.fetchone()

    if not user_data:
        return "❌ User not found. <a href='/add_user'>Add New User</a>"

    user_interests = set(i.strip().lower() for i in user_data[0].split(','))

    c.execute('SELECT name, interests FROM users WHERE email != ?', (email,))
    all_users = c.fetchall()

    recommendations = []
    for name, interests in all_users:
        other_interests = set(i.strip().lower() for i in interests.split(','))
        score = len(user_interests & other_interests)
        if score > 0:
            recommendations.append((name, score))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    peers = [r[0] for r in recommendations]

    conn.close()
    return render_template('recommend.html', peers=peers, email=email)

# 🧠 Test Route
@app.route('/test')
def test():
    return "✅ Flask is running fine!"

if __name__ == '__main__':
    print(f"🚀 Using database from: {DB_PATH}")
    app.run(debug=True)
