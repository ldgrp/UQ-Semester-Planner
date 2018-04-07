from helpers import get_soup
import re

URL = 'https://my.uq.edu.au/programs-courses/browse.html?level=ugpg' 

def scrape():
    programs = {}

    soup = get_soup(URL) 
    soup = soup.findAll('a', href=re.compile('acad_prog'))
    
    for a in soup:
        url = a['href']
        code = url[url.index('=')+1:]
        title = a.get_text(strip=True)
        programs[code] = title

    return programs

if __name__ == "__main__":
    print(scrape())
