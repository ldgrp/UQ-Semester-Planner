from uqsemplanner import app, db
from uqsemplanner import scripts

from flask import g, abort

class Course(db.Model):
    code = db.Column(db.Text, primary_key=True, nullable=False)
    title = db.Column(db.Text, nullable=False)
    incompatible = db.Column(db.Text)
    prerequsite = db.Column(db.Text)
    recommended_prerequsite = db.Column(db.Text)

    def __repr__(self):
        return "<Course {}>".format(self.code)

class Program(db.Model):
    code = db.Column(db.Text, primary_key=True, nullable=False)
    title = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Program {}>".format(self.code)

class Major(db.Model):
    code = db.Column(db.Text, primary_key=True, nullable=False)
    title = db.Column(db.Text, nullable=False)
    pcode = db.ForeignKey('db.code')

    def __repr__(self):
        return "<Major {}>".format(self.code)

#========================================
#========================================

def init_db():
    db.create_all()

def populate_db():
    courses = scripts.course.scrape()
    
    for c in courses:
        course = Course(code=c.code, title=c.title)
        db.session.add(course)
    print('Populated database with courses')
    
    programs = scripts.program.scrape()
    majors = {}

    for p in programs:
        program = Program(code=p.code, title=p.title)
        db.session.add(program)
        for m in p.get_majors():
            major = Major(code=m.code, title=m.title, pcode=p.code)
            db.session.add(major)

    print('Populated database with programs and majors')
    db.session.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.cli.command('populatedb')
def populatedb_command():
    populate_db()

#========================================
#========================================

def is_course_code(code):
    res = db.query.filter_by(code=code).first()

    if res is None:
        return False
    return True

def get_course_title(code):
    res = Course.query.filter_by(code=code).first()
    
    if res is None:
        abort(404)

    return res.title

def get_program(code):
    res = Program.query.filter_by(code=code).first()
    if res is None:
        abort(404)
    return res

def get_major(code):
    res = Major.query.filter_by(code=code).first()
    if res is None:
        abort(404)
    return res
