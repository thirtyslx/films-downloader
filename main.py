from PyQt5.QtWidgets import QApplication, QMainWindow
import sqlite3
import sys
import os
from mainWindow import Ui_MainWindow
from search import Search
from create_db import Create_db


class Piracy(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Creating users database
        no_database = 0
        if not os.path.isfile('films.db'): no_database = 1
        self.con = sqlite3.connect('users.db')
        self.cur = self.con.cursor()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()
        self.search = Search(self)
        self.current_user = ''
        if no_database: self.no_database_error()

    def initUI(self):
        """function for ui"""
        self.change_layer(0)
        # layer 0 (Login Manager)
        self.ui.l0_btn_login.clicked.connect(self.login)
        self.ui.l0_btn_register.clicked.connect(self.register)
        # layer 1 (Database not found Error)
        self.ui.l1_btn_exit.clicked.connect(app.quit)
        self.ui.l1_btn_create_db.clicked.connect(lambda _: self.change_layer(2))
        # layer 2 (Creating database)
        self.ui.l2_btn_start_creating_db.clicked.connect(lambda _: Create_db.create_db(Create_db(), 1, 1467, False))
        self.ui.l2_btn_back.clicked.connect(lambda _: self.change_layer(1))
        # layer 3 (Main page)
        self.ui.l3_btn_search_by_title.clicked.connect(lambda _: Search.click_event(self.search, 'title'))
        self.ui.l3_btn_search_by_title.clicked.connect(lambda _: self.change_layer(4))
        self.ui.l3_btn_search_by_description.clicked.connect(lambda _: Search.click_event(self.search, 'description'))
        self.ui.l3_btn_search_by_description.clicked.connect(lambda _: self.change_layer(4))
        self.ui.l3_btn_search_random.clicked.connect(lambda _: Search.click_event(self.search, 'random'))
        self.ui.l3_btn_search_random.clicked.connect(lambda _: self.change_layer(4))
        self.ui.l3_btn_search_random.clicked.connect(lambda _: self.ui.l4_btn_search.setFocus())
        self.ui.l3_btn_back.clicked.connect(lambda _: self.btn_back())
        self.ui.l3_btn_history.clicked.connect(lambda _: self.btn_history())
        # layer 4 (Search page)
        self.ui.l4_btn_back.clicked.connect(lambda _: self.change_layer(3))
        self.ui.l4_btn_back.clicked.connect(lambda _: self.ui.l4_search_res_text_edit.setText(''))
        self.ui.l4_btn_back.clicked.connect(lambda _: self.ui.l4_search_line_edit.setText(''))
        self.ui.l4_btn_search.clicked.connect(lambda _: self.btn_search())
        # layer 5 (History)
        self.ui.l5_btn_back.clicked.connect(lambda _: self.change_layer(3))
        self.ui.l5_btn_clear.clicked.connect(lambda _: self.btn_clear())

    def no_database_error(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT)
        """)
        self.con.commit()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS history (
            id INTEGER,
            search TEXT)
        """)
        self.con.commit()
        self.change_layer(1)

    def btn_back(self):
        """function for loging out"""
        self.change_layer(0)
        print(f'[login] Good bye, {self.current_user}!')
        self.change_user('')
        self.ui.l0_label_verdict.setText('Logged out!')

    def btn_search(self):
        """function for searching"""
        if self.ui.l4_search_line_edit.text() != '':
            self.cur.execute("""
                INSERT INTO history (id, search)
                VALUES ((SELECT id FROM users WHERE username = ?), ?)
            """, (self.current_user, self.ui.l4_search_line_edit.text()))
            self.con.commit()
        Search.search(self.search, self.ui.l4_search_line_edit.text())

    def change_layer(self, n):
        """function for changing ui layer"""
        layer_dict = {
            0: ['l0_btn_login', 'l0_btn_register', 'l0_label_password', 'l0_label_splash', 'l0_label_username',
                'l0_label_verdict', 'l0_password_line_edit', 'l0_username_line_edit'],
            1: ['l1_btn_create_db', 'l1_btn_exit', 'l1_label_error', 'l1_label_error_message'],
            2: ['l2_btn_start_creating_db', 'l2_label_log', 'l2_log_text_edit', 'l2_btn_back', 'l2_label_message'],
            3: ['l3_btn_search_by_description', 'l3_btn_search_by_title', 'l3_btn_search_random', 'l3_label_search',
                'l3_btn_back', 'l3_btn_history'],
            4: ['l4_btn_back', 'l4_btn_search', 'l4_label_search_results', 'l4_search_line_edit',
                'l4_search_res_text_edit'],
            5: ['l5_btn_back', 'l5_history_text_edit', 'l5_label_history', 'l5_btn_clear']
        }
        for key in layer_dict.keys():
            if key == n:
                for el in layer_dict[key]:
                    eval(f'self.ui.{el}.show()')
            else:
                for el in layer_dict[key]:
                    eval(f'self.ui.{el}.hide()')
        if n == 0:
            self.resize(1000, 360)
            self.ui.l0_username_line_edit.setFocus()
        elif n == 1:
            self.resize(1000, 750)
            self.ui.l1_btn_create_db.setFocus()
        elif n == 2:
            self.resize(1000, 410)
            self.ui.l2_btn_start_creating_db.setFocus()
        elif n == 3:
            self.resize(1000, 360)
            self.ui.l3_btn_search_by_title.setFocus()
        elif n == 4:
            self.resize(1000, 750)
            self.ui.l4_search_line_edit.setFocus()
        elif n == 5:
            self.resize(1000, 750)
            self.ui.l4_search_line_edit.setFocus()

    def login(self):
        """function for login"""
        username = self.ui.l0_username_line_edit.text()
        password = self.ui.l0_password_line_edit.text()
        verdict = self.ui.l0_label_verdict
        if username == '':
            verdict.setText('Username can\'t be empty')
        elif len(self.cur.execute("""SELECT username FROM users WHERE username = ?""", (username,)).fetchall()) != 0:
            if password == '':
                verdict.setText('Password can\'t be empty!')
            elif (password,) == \
                    self.cur.execute(""" SELECT password FROM users WHERE username = ?""", (username,)).fetchall()[0]:
                self.change_user(username)
                print(f'[login] Hello, {username}!')
                verdict.setText('Successfully logged in!')
                self.change_layer(3)
            else:
                verdict.setText('Wrong password!')
        else:
            verdict.setText('Invalid username')

    def register(self):
        """function for register"""
        username = self.ui.l0_username_line_edit.text()
        password = self.ui.l0_password_line_edit.text()
        verdict = self.ui.l0_label_verdict
        if username == '':
            verdict.setText('Username can\'t be empty')
        elif (username,) in self.cur.execute("""SELECT username FROM users""").fetchall():
            verdict.setText('Username is taken!')
        elif password == '':
            verdict.setText('Password can\'t be empty!')
        else:
            self.cur.execute("""
                             INSERT INTO users (username, password)
                             VALUES(?, ?)
                             """, (username, password))
            self.con.commit()
            print(f'[login] Hello, {username}!')
            self.change_user(username)
            verdict.setText('Registred!')
            self.change_layer(3)

    def change_user(self, username):
        """function for changing current user value"""
        self.current_user = username
        self.ui.l0_username_line_edit.setText('')
        self.ui.l0_password_line_edit.setText('')

    def btn_history(self):
        """function for history"""
        self.change_layer(5)
        res = self.cur.execute("""
            SELECT search FROM history WHERE id = (SELECT id FROM users WHERE username = ?)
       """, (self.current_user,)).fetchall()
        history = list()
        for i in range(len(list(res))):
            history.append(f'{i + 1}. {res[i][0]}\n')
        self.ui.l5_history_text_edit.setText(''.join(history))

    def btn_clear(self):
        """function for clearing history"""
        self.cur.execute("""
            DELETE FROM history WHERE id = (SELECT id FROM users WHERE username = ?)
        """, (self.current_user,))
        self.con.commit()
        self.ui.l5_history_text_edit.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = Piracy()
    p.show()
    sys.exit(app.exec())
#     _            ____                 _
#    / \   ___ ___| __ ) _ __ ___  __ _| | _____ _ __
#   / _ \ / __/ __|  _ \| '__/ _ \/ _` | |/ / _ \ '__|
#  / ___ \\__ \__ \ |_) | | |  __/ (_| |   <  __/ |
# /_/   \_\___/___/____/|_|  \___|\__,_|_|\_\___|_|
#
# http://www.gitlab.com/assbreaker/
#
# Main script for GUI
