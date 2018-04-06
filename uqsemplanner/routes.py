from uqsemplanner import app
from uqsemplanner.database import get_course_title
from flask import abort
from flask_restful import Api, Resource

api = Api(app, catch_all_404s=True)

class Course(Resource):
    def get(self, code):
        code = code.upper()
        title = get_course_title(code)
        return {'code': code, 'title': title}

    def put(self, code):
        return {code: code}
api.add_resource(Course, '/api/<string:code>')
