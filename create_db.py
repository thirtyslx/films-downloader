from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import sqlite3


class Create_db:
    """class for generating films database with error handler"""
    def __init__(self):
        self.con = sqlite3.connect('films.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY,
            source TEXT,
            title TEXT,
            title_lower TEXT,
            year INTEGER,
            link TEXT,
            description TEXT,
            description_lower TEXT
        )""")
        self.con.commit()
        user_agent = UserAgent(cache=False).random
        self.headers = {'User-Agent': user_agent}
        self.source = 'https://25-hd.lorfil.lol'
        self.url = f'{self.source}/filmy'
        self.error_list = []

    def create_db(self, start, end, areErrors=False):
        """function for generating films database with error handler"""
        if areErrors:
            page_list = self.error_list
            self.error_list = []
        else:
            page_list = range(start, end)
        for n in page_list:
            try:
                page = BeautifulSoup(requests.get(url=f'{self.url}/page/{n}', headers=self.headers).text, 'lxml')
                title_list = list()
                year_list = list()
                link_list = list()
                description_list = list()
                for title in page.find_all('div', class_='th-title'):
                    print(title.text)
                    title_list.append(title.text)
                for year in page.find_all('div', class_='th-year'):
                    print(year.text)
                    year_list.append(year.text)
                for film in page.find_all('div', class_='th-item'):
                    link = film.find('a', class_='th-in with-mask').get('href')
                    print(link)
                    link_list.append(link)
                for link in link_list:
                    film_page = BeautifulSoup(requests.get(
                        link, headers=self.headers).text, 'lxml')
                    description = film_page.find(
                        'div', class_='fdesc clearfix slice-this').text.strip()
                    print(f'"{description}"')
                    description_list.append(description)
                for i in range(len(title_list)):
                    title = title_list[i]
                    year = year_list[i]
                    description = description_list[i]
                    link = link_list[i]
                    self.cur.execute("""
                        INSERT INTO films (source, title, title_lower, year, description, description_lower, link)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (self.source, title, title.lower(), year, description, description.lower(), link))
                    self.con.commit()
                    print(f'Added {n + 1}.{i + 1}...')
            except:
                print(f'ERROR: failed downloading {n + 1} page')
                self.error_list.append(n)
        if len(self.error_list) != 0:
            self.create_db(0, 0, True)


if __name__ == '__main__':
    db = Create_db()
    db.create_db(1, 1467)
    print(db.error_list)
#                      _             _       _        _
#   ___ _ __ ___  __ _| |_ ___    __| | __ _| |_ __ _| |__   __ _ ___  ___
#  / __| '__/ _ \/ _` | __/ _ \  / _` |/ _` | __/ _` | '_ \ / _` / __|/ _ \
# | (__| | |  __/ (_| | ||  __/ | (_| | (_| | || (_| | |_) | (_| \__ \  __/
#  \___|_|  \___|\__,_|\__\___|  \__,_|\__,_|\__\__,_|_.__/ \__,_|___/\___|
#
# http://www.gitlab.com/assbreaker/
#
# Script for generating films database
