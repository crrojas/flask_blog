# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite3
from flask import (
    Flask,
    render_template,
    url_for,
    request,
    flash,
    redirect)

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

@app.route('/form', methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        db = connect_db()
        db.execute(
            'INSERT INTO entry (title, description) values (?, ?)',
            [title, description])
        db.commit()
        db.close()
        return u"Operación exitosa"
    else:
        return "Acceso denegado"


if __name__ == "__main__":
    app.run(debug=True)















