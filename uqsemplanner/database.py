from uqsemplanner import app
from uqsemplanner.scripts import scrape_courses

import sqlite3
from flask import g, abort

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.cli.command('populatedb_course')
def populatedb_course_command():
    courses = scrape_courses()
    
    db = get_db()
    db.execute('delete from courses')
    for (code, name) in courses:
        db.execute('insert into courses (code, title) values (?, ?)',
                [code, name])
    db.commit()
    print('Populated database with courses')

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the current
    application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#========================================
#========================================

def is_course_code(code):
    db = get_db()
    cur = db.execute('select code from courses where code=?', [code])
    res = cur.fetchone()

    if res is None:
        return False
    return True

def get_course_title(code):
    db = get_db()
    cur = db.execute('select title from courses where code=?', [code])
    res = cur.fetchone()
    
    if res is None:
        abort(404)

    return res['title']
