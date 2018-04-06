from uqsemplanner.database import is_course_code

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

def course_can_be_taken(course_code, history):
    info = get_course_info(course_code)
    prerequisite = info["prerequisite"]
    incompatible = info["incompatible"]
    
    if is_incompatible(incompatible, history):
        return False
    
    return satisfies_prerequisite(prerequisite, history)

def parse_course_info(info):
    info = info.replace(',', ' or ')
    info = info.replace('+', ' and ')

    words = re.findall(r"[\w']+", info)
    courses = []

    for word in words:
        if is_course_code(word):
            courses.append(word)
        elif len(word) == 8 and word[:4].isalpha() and word[4:8].isdigit():
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

