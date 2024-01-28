from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

# Database setup
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('todo.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Routes
@app.route('/')
def index():
    tasks = get_db().execute('SELECT * FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    get_db().execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    get_db().commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    get_db().execute('DELETE FROM tasks WHERE id=?', (id,))
    get_db().commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5003)
