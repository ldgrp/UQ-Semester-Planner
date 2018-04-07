from helpers import get_soup
import re

URL = 'https://my.uq.edu.au/programs-courses/browse.html?level=ugpg' 

class Program:
    def __init__(self, code, title):
        self.code = code
        self.title = title
        self.plans = []

    def add_plan(self, plan):
        self.plans.append(plan)

    def add_plans(self, plans):
        for plan in plans:
            self.add_plan(plan)

    def get_plans(self):
        return self.plans

class Plan:
    def __init__(self, code, title):
        self.code = code
        self.title = title

def scrape():
    programs = []
    plans = [] 

    soup = get_soup(URL) 
    a_acad_prog = soup.findAll('a', href=re.compile('acad_prog'))
    a_acad_plan = soup.findAll('a', href=re.compile('acad_plan'))

    for a in a_acad_plan:
        url = a['href']
        code = url[url.index('=')+1:]
        title = a.get_text(strip=True)
        plan = Plan(code, title)
        plans.append(plan)

    for a in a_acad_prog:
        url = a['href']
        code = url[url.index('=')+1:]
        title = a.get_text(strip=True)

        program = Program(code, title)

        majors = [plan for plan in plans if code in plan.code]
        program.add_plans(majors)
        programs.append(program)

    return programs

if __name__ == "__main__":
    programs = scrape()
    for program in programs:
        print("{}-{}".format(program.code, program.title))
        for plan in program.get_plans():
            print("\t{}".format(plan.title))
