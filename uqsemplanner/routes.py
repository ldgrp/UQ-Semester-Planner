from uqsemplanner import app
from uqsemplanner.course import course_can_be_taken
from uqsemplanner.database import get_course_title

from flask import abort, request
from flask_restful import Api, Resource

api = Api(app, catch_all_404s=True)

class Course(Resource):
    def get(self, code):
        code = code.upper()
        title = get_course_title(code)
        return {'code': code, 'title': title}

class CourseChecker(Resource):
    def post(self):
        history, code = None, None

        req_data = request.get_json(force=True)
        if 'history' in req_data and 'code' in req_data:
            code = req_data['code']
            history = req_data['history']
        else:
            abort(400)
        res = course_can_be_taken(code, history)
        return {'course_can_be_taken': res}

api.add_resource(CourseChecker, '/api/course/')
api.add_resource(Course, '/api/course/<string:code>')
