import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
import sqlite3
from kivymd.app import MDApp
from travel_planner_mapview import TravelPlannerMapView
from gps_helper import GPSHelper
from search_popup_menu import SearchPopupMenu
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
kivy.require("1.11.1")


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


class MainApp(MDApp):
    conn = None
    cur = None
    search_menu = None

    def on_start(self):

        # Login popup
        popupWindow = LogInPopup(title="Sign In", auto_dismiss=False, size_hint=(None, None), size=(400, 400))
        popupWindow.open()

        # GPS init
        GPSHelper().run()

        # Database init
        self.conn = sqlite3.connect("travel_planner.db")
        self.cur = self.conn.cursor()

        # Search Menu init
        self.search_menu = SearchPopupMenu()


if __name__ == '__main__':
    MainApp().run()
