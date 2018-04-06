from uqsemplanner import app
from uqsemplanner.course import course_can_be_taken, get_course_info
from uqsemplanner.database import get_course_title

from flask import abort, request
from flask_restful import Api, Resource

api = Api(app, catch_all_404s=True)

class Course(Resource):
    def get(self, code):
        code = code.upper()
        title = get_course_title(code)
        return {'code': code, 'title': title}

    def post(self, code):
        history = None
        code = code.upper()
        req_data = request.get_json(force=True)
        if 'history' in req_data:
            history = req_data['history']
        else:
            abort(400)
        info = get_course_info(code)
        res = course_can_be_taken(info, history)
        return {'course_can_be_taken': res}

api.add_resource(Course, '/api/<string:code>')
