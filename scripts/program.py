from helpers import get_soup
import re

URL = 'https://my.uq.edu.au/programs-courses/browse.html?level=ugpg' 

class Program:
    def __init__(self, code, title):
        self.code = code
        self.title = title
        self.majors = []

    def add_major(self, major):
        self.majors.append(major)

    def add_majors(self, majors):
        for major in majors:
            self.add_major(major)

    def get_majors(self):
        return self.majors

class Major:
    def __init__(self, code, title):
        self.code = code
        self.title = title

def scrape():
    programs = []
    majors = [] 

    soup = get_soup(URL) 
    a_acad_prog = soup.findAll('a', href=re.compile('acad_prog'))
    a_acad_plan = soup.findAll('a', href=re.compile('acad_plan'))

    for a in a_acad_plan:
        url = a['href']
        code = url[url.index('=')+1:]
        title = a.get_text(strip=True)
        major = Major(code, title)
        majors.append(major)

    for a in a_acad_prog:
        url = a['href']
        code = url[url.index('=')+1:]
        title = a.get_text(strip=True)

        program = Program(code, title)

        program_majors = [major for major in majors if code in major.code]
        program.add_majors(program_majors)
        programs.append(program)

    return programs

if __name__ == "__main__":
    programs = scrape()
    for program in programs:
        print("{}-{}".format(program.code, program.title))
        for major in program.get_majors():
            print("\t{}".format(major.title))
