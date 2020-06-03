import kivy
import sqlite3
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from travel_planner_mapview import TravelPlannerMapView
from gps_helper import GPSHelper
from search_popup_menu import SearchPopupMenu
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from login_popup import LogInPopup
from register_popup import RegisterPopup

kivy.require("1.11.1")


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    sign_in = ObjectProperty()
    register = ObjectProperty()
    list = ObjectProperty()
    my_trips = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_in_popup = LogInPopup(title="Sign In", auto_dismiss=False, size_hint=(None, None), size=(400, 400))
        self.log_in_popup.bind(on_dismiss=self.set_cur_user)
        self.register_popup = RegisterPopup(title="Register", auto_dismiss=False, size_hint=(None, None), size=(400, 400))
        self.register_popup.bind(on_dismiss=self.set_cur_user)
        self.currUser = None

    def set_cur_user(self, popup):
        if self.log_in_popup.currUser != "":
            self.currUser = self.log_in_popup.currUser
            print("Logged in as", self.currUser)
            self.list.remove_widget(self.sign_in)
            self.list.remove_widget(self.register)
            self.list.add_widget(OneLineListItem(text="My Trips", id="my_trips"))

        elif self.register_popup.currUser != "":
            self.currUser = self.register_popup.currUser
            print("Logged in as", self.currUser)


class MainApp(MDApp):
    conn = None
    cur = None
    search_menu = None

    def on_start(self):
        # GPS init
        GPSHelper().run()

        # Database init
        self.conn = sqlite3.connect("travel_planner.db")
        self.cur = self.conn.cursor()

        # Search Menu init
        self.search_menu = SearchPopupMenu()


if __name__ == '__main__':
    MainApp().run()
