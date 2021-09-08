import requests
from bs4 import BeautifulSoup

import re
import os
import json

URL = 'https://stihi.ru'
PATH = 'D:/stihi'

    
def getData(path):
    with open(path, 'r+') as file:
        data = json.loads(file.read())
        file.close
        return data

def setData(path, data):
    with open(path, 'w+') as file:
        json.dump(data, file)
        file.close
        return True

def poem(url, author):
    data = []
    if os.path.exists('{0}/{1}/db.json'.format(PATH, author)):
        data = getData('{0}/{1}/db.json'.format(PATH, author))
    if url in data:
        pass
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    poem_name = soup.find('h1')
    poem = soup.find('div', class_='text')
    data.append(url)
    setData('{0}/{1}/db.json'.format(PATH, author), data)
    return (poem_name.text,poem.text)

def book(url, bookLink, page = 0, poemLinks = {}):

    response = requests.get(url + '&s={0}'.format(page) + '&{0}'.format(bookLink))
    soup = BeautifulSoup(response.text, 'lxml')
    poems = soup.find_all('a', class_='poemlink')

    for poem in poems:
        poemLink = poem.get('href')
        poemName = poem.text
        poemLinks.update({poemName: poemLink})

    if len(poems) != 0:
        poemLinks = book(url, page + 50, poemLinks)

    return poemLinks

def author(url, page = 0):

    poems = authorPage(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    books = soup.find_all('div', id='bookheader')
    authorName = soup.find('h1').text
    for b in books:
        bookl = b.find('a').get('href')
        bookLink = re.match(r'/avtor/.+&(.+)', bookl)
        poems.update(book(url, bookLink))
    return (authorName, poems)
        
    

def authorPage(url, page = 0, poemLinks = {}):

    response = requests.get(url + '&s={0}'.format(page))
    soup = BeautifulSoup(response.text, 'lxml')
    poems = soup.find_all('a', class_='poemlink')
    for poem in poems:
        poemLink = poem.get('href')
        poemName = poem.text
        poemLinks.update({poemName: poemLink})
    
    if len(poems) != 0:
        poemLinks = authorPage(url, page + 50, poemLinks)

    return poemLinks


authorpg = author('https://stihi.ru/avtor/budarin')
if not os.path.exists('{0}/{1}'.format(PATH, authorpg[0])):
    os.mkdir('{0}/{1}'.format(PATH, authorpg[0]))

for name in authorpg[1]:
    pm = poem(URL + authorpg[1][name], authorpg[0])
    file = open('{0}/{1}/'.format(PATH, authorpg[0]) +re.sub('[/|\:*?<>]','',pm[0]) + '.txt', 'w', encoding='UTF-8')
    file.write(pm[1])
    file.close()
