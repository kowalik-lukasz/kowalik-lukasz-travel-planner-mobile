import sqlite3
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
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

        # find_user = ("SELECT * FROM users WHERE username = ? AND password = ?")
        # self.cur.execute(find_user, [self.username.text, self.password.text])
        # results = self.cur.fetchall()

        """
        Example Use of calculating route

        route = {'Start_point': 'Wrocław', 'Mid_points': 'Kraków,gdańsk,warszawa,Katowice,malbork', 'End_point': 'wrocław', 'mobile': 'true', 'user': r.text}
        r = requests.post('http://127.0.0.1:8000/planner/plan_journey/', data=route)
        print(r)
        """

        # if results:
        if 'Logged In' in r.text:
            self.dismiss()
            self.conn.close()
        else:
            self.error_message.visible = True