import sqlite3
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivymd.app import App
import requests


class LogInPopup(Popup):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    error_message = ObjectProperty(None)
    conn = None
    cur = None
    currUser = ""

    def log_in_check(self):
        self.conn = sqlite3.connect("travel_planner.db")
        self.cur = self.conn.cursor()

        credentials = {'username': self.username.text, 'password': self.password.text, 'mobile': 'true'}
        r = requests.post('http://127.0.0.1:8000/planner/user_login/', data=credentials)

        self.username.text = ""
        self.password.text = ""

        if 'Logged In' in r.text:
            self.currUser = r.text[10:]
            self.dismiss()
            self.conn.close()
        else:
            self.error_message.visible = True

    def dismiss_popup(self):
        self.error_message.visible = False
        self.currUser = ""
        self.dismiss()
