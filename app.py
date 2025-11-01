from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime


app = Flask(__name__)

# ---------------- Database Setup ---------------- #
def init_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()


# ---------------- Routes ---------------- #
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes ORDER BY id ASC")
    notes = [
        {"id": row[0], "title": row[1], "content": row[2], "created_at": row[3]}
        for row in c.fetchall()
    ]
    conn.close()
    return jsonify(notes)


@app.route('/add_note', methods=['POST'])
def add_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)",
              (title, content, created_at))
    conn.commit()
    conn.close()
    return jsonify({"message": "Note added successfully"})


@app.route('/update_note/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, note_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Note updated"})


@app.route('/delete_note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Note deleted"})


if __name__ == '__main__':
    app.run(debug=True)
