import kivy
import sqlite3
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from travel_planner_mapview import TravelPlannerMapView
from gps_helper import GPSHelper
from search_popup_menu import SearchPopupMenu
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from login_popup import LogInPopup

kivy.require("1.11.1")


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


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
