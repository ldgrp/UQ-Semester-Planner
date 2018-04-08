from .helpers import get_soup
import csv
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

    def __hash__(self):
        return hash((self.code, self.title))

    def __eq__(self, other):
        return self.code == other.code

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

    return set(programs)

PROGRAMS_FILE = 'output/programs.csv'
MAJORS_FILE = 'output/majors.csv'

if __name__ == "__main__":
    programs = scrape()
    majors = {}

    with open(PROGRAMS_FILE, 'w') as programfile:
        programwrite = csv.writer(programfile)
        for program in programs:
            programwrite.writerow([program.code, program.title])
            majors[program.code] = program.get_majors()
    with open(MAJORS_FILE, 'w') as majorfile:
        majorwrite = csv.writer(majorfile)
        for pcode, majorlist in majors.items():
            for major in majorlist:
                majorwrite.writerow([major.code, major.title, pcode])

    print("UQ Program List output to ", PROGRAMS_FILE)
    print("UQ Majors List output to", MAJORS_FILE)
