import requests
from bs4 import BeautifulSoup
from requests.api import request
import re

URL = 'https://stihi.ru'

    

def poem(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    poem_name = soup.find('h1')
    poem = soup.find('div', class_='text')
    return (poem_name.text,poem.text)

def books(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    poems = soup.find_all('a', class_='poemlink')
    poem_links = []

    for poem in poems:
        poem_link = poem.get('href')
        poem_links.append(poem_link)

    return poem_links

def author(url, page = 0):

    poems = authorPage

def authorPage(url, page = 0, poemLinks = {}):

    response = requests.get(url + '&s={0}'.format(page))
    soup = BeautifulSoup(response.text, 'lxml')
    poems = soup.find_all('a', class_='poemlink')
    for poem in poems:
        poemLink = poem.get('href')
        poemName = poem.text
        poemLinks.update({poemName: poemLink})
    
    return poemLinks
    

    



#urls = author_page('https://stihi.ru/avtor/budarin')
#for url in urls:
#    pm = poem(URL + url)
#    file = open(pm[0], 'w')
#    file.write(pm[1])
#
