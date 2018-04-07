from bs4 import BeautifulSoup
from urllib import request

def get_soup(url):
    html = request.urlopen(url)
    soup = BeautifulSoup(html.read(), 'html.parser')

    return soup
