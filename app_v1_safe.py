"""
Simple Flask API - Initial Safe Version
This is the base code in the repo
"""

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'alice', 'alice@example.com', 1000.0)")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'bob', 'bob@example.com', 500.0)")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({'message': 'Payment API v1.0', 'status': 'running'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    init_db()
    print("Starting Payment API on http://localhost:5000")
    app.run(debug=True, port=5000)
