from flask import render_template

from uqsemplanner import app
from uqsemplanner.uqsemplanner import get_db

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('select code, title from courses order by id')
    entries = cur.fetchall()
    return render_template('show_course_list.html', entries=entries)
