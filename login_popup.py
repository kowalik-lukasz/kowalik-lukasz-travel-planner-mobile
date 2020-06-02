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

    def log_in_check(self):
        self.conn = sqlite3.connect("travel_planner.db")
        self.cur = self.conn.cursor()

        credentials = {'username': self.username.text, 'password': self.password.text, 'mobile': 'true'}
        r = requests.post('http://127.0.0.1:8000/planner/user_login/', data=credentials)

        if 'Logged In' in r.text:
            app = App.get_running_app()
            app.username = self.username.text
            self.dismiss()
            self.conn.close()
        else:
            self.error_message.visible = True
