from helpers import get_soup
import csv
import re

URL = "https://my.uq.edu.au/programs-courses/course.html?course_code="

class Course:
    def __init__(self, code, title=None):
        self.code = code
        self.title = title

        self.prerequisite = None
        self.incompatible = None
        self.recommended_prerequisite = None
        self.restriction = None
    
    def add_incompatible(self, incompatible):
        self.incompatible = incompatible

    def add_prerequisite(self, prerequisite):
        self.prerequisite = prerequisite

    def add_recommended_prerequisite(self, r_prerequisite):
        self.recommended_prerequisite = r_prerequisite

    def add_restriction(self, restriction):
        pass

    def set_title(self, title):
        self.title = title

class CourseCondition:
    def __init__(self, raw_condition):
        self.raw_condition = raw_condition
        self.process()

    def process():
        pass

def scrape_course_info(course):
    soup = get_soup(URL + course.code)

    if soup.find(id="course-notfound"):
        raise ValueError("Course code not found")
    

    conditions = [
            "course-incompatible",
            "course-prerequisite",
            "course-recommended-prerequisite"
    ]
    conditions = [soup.find(id=condition).get_text(strip=True) for condition in conditions]

    incompatibles = CourseCondition(condition[0])
    prerequisites = CourseCondition(condition[1])
    r_prerequisites = CourseCondition(condition[2])

    title = soup.find(id='course-title').get_text(strip=True)
    course.set_title(title)

    course.add_incompatible(incompatible)
    course.add_prerequisite(prerequisite)
    course.add_recommended_prerequisite(r_prerequisites)

    return course

def parse_course_info(info):
    info = info.replace(',', ' or ')
    info = info.replace('+', ' and ')

    words = re.findall(r"[\w']+", info)
    courses = []

    for word in words:
        if is_course_code(word):
            courses.append(word)
        elif word not in ['or', 'and']:
            raise ValueError("Unexpected word '" + word + "'  while parsing course info.")
    return info, courses 

def satisfies_prerequisite(prerequisite, history):
    expr, courses = parse_course_info(prerequisite)
    
    courses = [course for course in courses if course not in history]
    courses = {course: False for course in courses}
    history = {course: True for course in history}
    history.update(courses)

    result = eval(expr, {}, history) # WARNING: DANGEROUS FUNCTION
    return result

def is_incompatible(incompatible, history):
    _,courses = parse_course_info(incompatible)
    for course in courses:
        if course in history:
            return True 
    return False

def course_can_be_taken(info, history):
    prerequisite = info["prerequisite"]
    incompatible = info["incompatible"]
    
    if is_incompatible(incompatible, history):
        return False
    
    return satisfies_prerequisite(prerequisite, history)
    
    
def is_course_code(string):
    return string in COURSE_CODES
    # return len(string) == 8 and \
    #        string[:4].isalpha() and \
    #        string[4:8].isdigit()
