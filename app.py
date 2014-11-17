# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def connect_db():
    """Retorna una conexión a la BD"""
    path_to_db = 'entry.db'
    rv = sqlite3.connect(path_to_db)
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Crea las tablas y datos de prueba"""
    db = connect_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

@app.route('/')
def show_entries():
    db = connect_db()
    cur = db.execute('SELECT title, description FROM entry ORDER BY id DESC')
    entries = cur.fetchall()
    db.close()
    return render_template('entries.html', entries=entries)

if __name__ == "__main__":
    app.run(debug=True)















