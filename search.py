import sqlite3
from selenium.webdriver.common.by import By
import undetected_chromedriver


class Search:
    def __init__(self, s):
        # 's' is main ui class object
        self.s = s
        self.con = sqlite3.connect('films.db')
        self.cur = self.con.cursor()
        self.mode = ''
        self.search_result = list()

    def click_event(self, mode):
        'function for changing search mode'
        self.mode = mode
        print(f'[search-mode] {self.mode}')

    def search(self, message):
        'function for search in films database'
        title_list = list()
        year_list = list()
        link_list = list()
        description_list = list()
        print(f'[search] "{message}"')
        message = message.lower()
        if self.mode == 'random':
            res = self.cur.execute(
                'SELECT * FROM films WHERE id == (SELECT id FROM films ORDER BY RANDOM() LIMIT 1)').fetchall()[0]
            title_list.append(res[2])
            year_list.append(res[4])
            link_list.append(res[5])
            description_list.append(res[6])
        elif message == '':
            print('[ERROR] empty search input')
        elif self.mode == 'title':
            for title in self.cur.execute('SELECT title FROM films WHERE title_lower LIKE ?',
                                          (f'%{message}%',)).fetchall():
                title_list.append(title)
            for year in self.cur.execute('SELECT year FROM films WHERE title_lower LIKE ?',
                                         (f'%{message}%',)).fetchall():
                year_list.append(year)
            for link in self.cur.execute('SELECT link FROM films WHERE title_lower LIKE ?',
                                         (f'%{message}%',)).fetchall():
                link_list.append(link)
            for description in self.cur.execute('SELECT description FROM films WHERE title_lower LIKE ?',
                                                (f'%{message}%',)).fetchall():
                description_list.append(description)
        elif self.mode == 'description':
            for title in self.cur.execute('SELECT title FROM films WHERE description_lower LIKE ?',
                                          (f'%{message}%',)).fetchall():
                title_list.append(title)
            for year in self.cur.execute('SELECT year FROM films WHERE description_lower LIKE ?',
                                         (f'%{message}%',)).fetchall():
                year_list.append(year)
            for link in self.cur.execute('SELECT link FROM films WHERE description_lower LIKE ?',
                                         (f'%{message}%',)).fetchall():
                link_list.append(link)
            for description in self.cur.execute('SELECT description FROM films WHERE description_lower LIKE ?',
                                                (f'%{message}%',)).fetchall():
                description_list.append(description)
        print(f'[results-count] {len(title_list)}')
        if len(title_list) != 0:
            print('Searching, please wait.')
            self.s.ui.l4_search_res_text_edit.setText('Searching, please wait.')
            self.get_links(title_list, year_list, link_list, description_list)
        else:
            print('Nothing found!')
            self.s.ui.l4_search_res_text_edit.setText('Nothing found!')

    def get_links(self, title_list, year_list, link_list, description_list):
        'function for parsing films links'
        options = undetected_chromedriver.ChromeOptions()
        options.headless = True
        driver = undetected_chromedriver.Chrome(options=options)
        res_link_list = list()
        for link in link_list:
            try:
                if self.mode == 'random':
                    driver.get(link)
                else:
                    driver.get(link[0])
                driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
                element = driver.find_element(By.XPATH, """/html/body/div/pjsdiv/pjsdiv[1]/video""")
                film_link = str(element.get_attribute('src'))
                print(film_link)
                # changing films quiality
                # film_link = film_link.split('/240.mp4')
                # attribute = film_link[1]
                # film_link = film_link[0]
                # attribute = attribute.split('_')[0]
                # film_link = f'{film_link}/720.mp4{attribute}_720p.mp4'
                # print(film_link)
                res_link_list.append(film_link)
            except:
                print('[ERROR]')
                res_link_list.append('[ERROR]')
        driver.close()
        driver.quit()
        separator = '+------------------------------------------------------------+\n'
        self.search_result = []
        if self.mode == 'random':
            film = list()
            film.append(separator)
            film.append('\n')
            film.append(f'{title_list[0]}')
            film.append('\n')
            film.append('\n')
            film.append(f'{year_list[0]}')
            film.append('\n')
            film.append('\n')
            film.append(f'{description_list[0]}')
            film.append('\n')
            film.append('\n')
            # link to the orinal film page
            # film.append(link_list[i][0])
            # film.append('\n')
            # film.append('\n')
            film.append(f'{res_link_list[0]}')
            film.append('\n')
            self.search_result.append(''.join(film))
        else:
            for i in range(len(link_list)):
                film = list()
                film.append(separator)
                film.append('\n')
                film.append(f'{title_list[i][0]}')
                film.append('\n')
                film.append('\n')
                film.append(f'{year_list[i][0]}')
                film.append('\n')
                film.append('\n')
                film.append(f'{description_list[i][0]}')
                film.append('\n')
                film.append('\n')
                # link to the orinal film page
                # film.append(link_list[i][0])
                # film.append('\n')
                # film.append('\n')
                film.append(f'{res_link_list[i]}')
                film.append('\n')
                self.search_result.append(''.join(film))
        res = self.s.ui.l4_search_res_text_edit
        res.setText('')
        for el in self.search_result:
            print(el)
            res.setText(f"{res.toPlainText()}\n{el}")
        print(separator)
        res.setText(f"{res.toPlainText()}\n{separator}")
#                          _
#  ___  ___  __ _ _ __ ___| |__
# / __|/ _ \/ _` | '__/ __| '_ \
# \__ \  __/ (_| | | | (__| | | |
# |___/\___|\__,_|_|  \___|_| |_|
#
# http://www.gitlab.com/assbreaker/
#
# Script to search films in database
