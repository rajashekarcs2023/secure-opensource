"""
Vulnerable Demo Application
Intentionally contains SQL Injection vulnerability for demonstration
DO NOT use in production!
"""

import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize database
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
    # Add sample data
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'alice', 'alice@example.com', 1000.0)")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'bob', 'bob@example.com', 500.0)")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (3, 'charlie', 'charlie@example.com', 750.0)")
    conn.commit()
    conn.close()

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    VULNERABILITY: SQL Injection
    User input is directly concatenated into SQL query without sanitization
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABLE CODE - DO NOT DO THIS!
    query = f"SELECT * FROM users WHERE id = {user_id}"
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return jsonify({
                'id': result[0],
                'username': result[1],
                'email': result[2],
                'balance': result[3]
            })
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/transfer', methods=['POST'])
def transfer_money():
    """
    Another vulnerable endpoint with SQL injection
    """
    data = request.get_json()
    from_user = data.get('from_user_id')
    to_user = data.get('to_user_id')
    amount = data.get('amount')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Direct string concatenation
    query = f"UPDATE users SET balance = balance - {amount} WHERE id = {from_user}"
    
    try:
        cursor.execute(query)
        query2 = f"UPDATE users SET balance = balance + {amount} WHERE id = {to_user}"
        cursor.execute(query2)
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Transfer completed'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    print("⚠️  WARNING: This app contains intentional vulnerabilities for demo purposes")
    print("Starting vulnerable app on http://localhost:5000")
    app.run(debug=True, port=5000)
