"""
Secure Demo Application
SQL Injection vulnerabilities fixed
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
    Fixed: SQL Injection using parameterized query
    """
    try:
        user_id = int(user_id)  # Input validation: Ensure user_id is an integer
    except ValueError:
        return jsonify({'error': 'Invalid user ID'}), 400

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Fixed: Using parameterized query with ? placeholder
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    
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
    Fixed: SQL Injection using parameterized queries
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400

    try:
        from_user = int(data.get('from_user_id'))
        to_user = int(data.get('to_user_id'))
        amount = float(data.get('amount'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input types'}), 400

    if amount <= 0:
        return jsonify({'error': 'Invalid transfer amount'}), 400

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Fixed: Using parameterized queries with ? placeholders
    query = "SELECT balance FROM users WHERE id = ?"
    cursor.execute(query, (from_user,))
    from_balance = cursor.fetchone()
    
    if not from_balance or from_balance[0] < amount:
        conn.close()
        return jsonify({'error': 'Insufficient balance'}), 400

    try:
        # Fixed: Parameterized query for update
        query = "UPDATE users SET balance = balance - ? WHERE id = ?"
        cursor.execute(query, (amount, from_user))
        
        query = "UPDATE users SET balance = balance + ? WHERE id = ?"
        cursor.execute(query, (amount, to_user))
        
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Transfer completed'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    print("Starting secure app on http://localhost:5000")
    app.run(debug=True, port=5000)