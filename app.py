from flask import Flask, render_template, request, redirect
import sqlite3
import re

app = Flask(__name__)

def get_db():
    return sqlite3.connect("contacts.db")

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        address TEXT,
        email TEXT UNIQUE,
        phone TEXT
    )''')
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db()
    contacts = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        email = request.form['email']

        # Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid Email"

        conn = get_db()
        try:
            conn.execute("""
                INSERT INTO contacts (first_name, last_name, address, email, phone)
                VALUES (?, ?, ?, ?, ?)
            """, (
                request.form['first_name'],
                request.form['last_name'],
                request.form['address'],
                email,
                request.form['phone']
            ))
            conn.commit()
        except:
            return "Duplicate Email Not Allowed"

        conn.close()
        return redirect('/')

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()

    if request.method == 'POST':
        conn.execute("""
            UPDATE contacts
            SET first_name=?, last_name=?, address=?, email=?, phone=?
            WHERE id=?
        """, (
            request.form['first_name'],
            request.form['last_name'],
            request.form['address'],
            request.form['email'],
            request.form['phone'],
            id
        ))
        conn.commit()
        conn.close()
        return redirect('/')

    contact = conn.execute("SELECT * FROM contacts WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
