import sqlite3
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class LogInPopup(Popup):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    error_message = ObjectProperty(None)
    conn = None
    cur = None

    def log_in_check(self):
        self.conn = sqlite3.connect("travel_planner.db")
        self.cur = self.conn.cursor()

        find_user = ("SELECT * FROM users WHERE username = ? AND password = ?")
        self.cur.execute(find_user, [self.username.text, self.password.text])
        results = self.cur.fetchall()

        if results:
            self.dismiss()
            self.conn.close()
        else:
            self.error_message.visible = True
