from bs4 import BeautifulSoup
from urllib import request

import re

URL = "https://my.uq.edu.au/programs-courses/course.html?course_code="

def get_soup(course_code):
    html = request.urlopen(URL + course_code)
    soup = BeautifulSoup(html.read(), 'html.parser')
    
    if soup.find(id="course-notfound"):
        raise ValueError("Course code not found")
    return soup

def get_course_info(course_code):
    soup = get_soup(course_code)
    
    info = {
            "incompatible": soup.find(id="course-incompatible"),
            "prerequisite": soup.find(id="course-prerequisite"),
            "recommended-prerequisite": soup.find(id="course-recommended-prerequisite")
    }

    info = {k:v.get_text(strip="True") if v else None for (k,v) in info.items()}

    return info
def parse_course_info(info):
    re.sub(r'(?<=[+,])(?=[^\s])', r' ', info)
    info = info.replace(',', 'or')
    info = info.replace('+', 'and')

    words = re.findall(r"[\w']+", info)
    valid = True
    courses = []

    for word in words:
        if is_course_code(word):
            courses.append(word)
        else:
            valid = False
    return info, courses, valid 

def course_can_be_taken(history, info):
    history = {course: True for course in history}

    prereq = info["prerequisite"]
    incomp = info["incompatible"]
    
    _,incomp_courses,_ = parse_course_info(incomp)
    for course in incomp_courses:
        if course in history:
            return False
    
    prereq_expr, prereq_courses, prereq_status = parse_course_info(prereq)
    prereq_courses = [course for course in prereq_courses if course not in history]
    prereq_courses = {course: False for course in prereq_courses}

    history.update(prereq_courses)

    result = eval(prereq_expr, {}, history)
    return result
    
def is_course_code(string):
    return len(string) == 8 and \
            string[:4].isalpha() and \
            string[4:8].isdigit()
