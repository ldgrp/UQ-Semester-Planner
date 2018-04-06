from bs4 import BeautifulSoup
from urllib import request

import csv

FILE = "courses.csv"
URL = "https://my.uq.edu.au/programs-courses/search.html?keywords=+&searchType=all&archived=true&CourseParameters%5Bsemester%5D=#courses"

def scrape_courses():
    """Scrapes my.UQ to get course data.

    Return:
        list: Returns a list of 2-tuples.
    """
    courses = [] 
    # Fetch HTML
    html = request.urlopen(URL)
    soup = BeautifulSoup(html.read(), 'html.parser')

    codes = soup.findAll('a', 'code')
    
    for code in codes:
        name = code.nextSibling.nextSibling
        courses.append((
            code.get_text(strip=True),
            name.get_text(strip=True)
        ))

    return courses

if __name__ == "__main__":
    courses = scrape_courses()

    with open(FILE, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for course in courses:
            csvwriter.writerow(course)
        print("Data written to {}!".format(FILE))
