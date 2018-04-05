from bs4 import BeautifulSoup
from urllib import request

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

if __name__ == "__main__":
    user_input = input("Input course code: ")
    print(get_course_info(user_input))

