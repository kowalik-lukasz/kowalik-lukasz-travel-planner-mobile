import sqlite3
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
import requests


class RegisterPopup(Popup):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    error_message = ObjectProperty(None)
    conn = None
    cur = None
    currUser = ""

    def register_check(self):
        self.conn = sqlite3.connect("travel_planner.db")
        self.cur = self.conn.cursor()

        credentials = {'username': self.username.text, 'password': self.password.text, 'mobile': 'true'}
        r = requests.post('http://127.0.0.1:8000/planner/registration/', data=credentials)

        if 'Registered' in r.text:
            self.currUser = r.text[11:]
            self.dismiss()
            self.conn.close()
        else:
            self.error_message.visible = True
