from .helpers import get_soup
import csv
import re

COURSE_URL = "https://my.uq.edu.au/programs-courses/course.html?course_code="
COURSE_CATALOG_URL = "https://my.uq.edu.au/programs-courses/search.html?keywords=+&searchType=all&archived=true&CourseParameters%5Bsemester%5D=#courses"

class Course:
    def __init__(self, code, title=None):
        self.code = code
        self.title = title

        self.prerequisite = None
        self.incompatible = None
        self.recommended_prerequisite = None
        self.restriction = None
    
    def can_be_taken(self, history):
        if self.incompatible.evaluate(self, history):
            return False
        return self.prerequisite.evaluate(self, history)

    def scrape(self):
        soup = get_soup(COURSE_URL + self.code)

        if soup.find(id="course-notfound"):
            raise ValueError("Course code not found")

        self.scrape_conditions(soup)
        if not self.title:
            scrape_title(soup)
    
    def scrape_conditions(self, soup):
        condition_ids = [
                "course-incompatible",
                "course-prerequisite",
                "course-recommended-prerequisite"
        ]

        conditions = [soup.find(id=condition_id) for condition_id in condition_ids]
        conditions = [condition.get_text(strip=True) if condition else None for
                condition in conditions]

        incompatible = IncompatibleCondition(conditions[0])
        prerequisite = PrerequisiteCondition(conditions[1])
        r_prerequisite = PrerequisiteCondition(conditions[2])

        self.incompatible = incompatible
        self.prerequisite = prerequisite
        self.recommended_prerequisite = r_prerequisite

    def scrape_title(self, soup):
        title = soup.find(id='course-title').get_text(strip=True)
        self.title = title


class CourseCondition:
    def __init__(self, raw_condition):
        self.raw_condition = raw_condition
        self.condition = None
        self.courses = None

        if self.raw_condition:
            self.parse_raw_condition()

    def parse_raw_condition(self):
        condition = self.raw_condition
        condition = condition.replace(',', ' or ')
        condition = condition.replace('+', ' and ')
    
        #words = re.findall(r"[\w']+", info)
        #courses = []

        #for word in words:
        #    if is_course_code(word):
        #        courses.append(word)
        #    elif word not in ['or', 'and']:
        #        raise ValueError("Unexpected word '" + word + "'  while parsing course info.")
        self.condition = condition
        self.courses = None

    def evaluate(self, history):
        raise NotImplementedError()

class PrerequisiteCondition(CourseCondition):
    def evaluate(self, history):
        if not self.condition:
            raise Exception()
        courses = [course for course in self.courses if course not in history]
        courses = {course: False for course in courses}
        history = {course: True for course in history}
        history.update(courses)

        result = eval(expr, {}, history) # WARNING: DANGEROUS FUNCTION
        return result

class IncompatibleCondition(CourseCondition):
    def evaluate(self, history):
        for course in self.courses:
            if course in history:
                return True
        return False

def scrape():
    soup = get_soup(COURSE_CATALOG_URL)

    courses = []
    codes = soup.findAll('a', 'code')

    for code in codes:
        name = code.nextSibling.nextSibling.get_text(strip=True)
        course_code = code.get_text(strip=True)
        
        course = Course(course_code, name)
        courses.append(course)

    return courses

def is_course_code(string):
     return len(string) == 8 and \
            string[:4].isalpha() and \
            string[4:8].isdigit()

COURSES_FILE = 'output/courses.csv'

if __name__ == "__main__":
    courses = scrape()
    with open(COURSES_FILE, 'w') as coursefile:
        coursewriter = csv.writer(coursefile)
        for course in courses:
            coursewriter.writerow([course.code, course.title])

    print("UQ Course List output to ", COURSES_FILE)
