import kivy
import sqlite3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem, MDList
from travel_planner_mapview import TravelPlannerMapView
from gps_helper import GPSHelper
from search_popup_menu import SearchPopupMenu
from kivy.properties import ObjectProperty
from login_popup import LogInPopup
from route_maker import RouteMaker
from trip_viewer import TripViewer
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager
from register_popup import RegisterPopup


kivy.require("1.11.1")


class ScreenManagement(ScreenManager):
    pass


class MapScreen(Screen):
    def switch(self, screen):
        self.screen_manager.current = screen


class RouteMakerScreen(Screen):
    def switch(self, screen):
        self.screen_manager.current = screen


class MyTripsScreen(Screen):
    trip_viewer = ObjectProperty()

    def switch(self, screen):
        self.screen_manager.current = screen


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    sign_in = ObjectProperty()
    register = ObjectProperty()
    list = ObjectProperty()
    my_trips = None
    sign_out = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.log_in_popup = LogInPopup(title="Sign In", auto_dismiss=False, size_hint=(None, None), size=(400, 400),
                                       on_dismiss=self.set_cur_user)
        self.register_popup = RegisterPopup(title="Register", auto_dismiss=False, size_hint=(None, None), size=(400, 400),
                                            on_dismiss=self.set_cur_user)

    def set_cur_user(self, popup):
        if self.log_in_popup.currUser != "" or self.register_popup.currUser != "":
            if self.log_in_popup.currUser != "":
                self.log_in_popup.error_message.visible = False
                self.login_menu_list(self.log_in_popup.currUser)
            else:
                self.register_popup.error_message.visible = False
                self.login_menu_list(self.register_popup.currUser)

    def login_menu_list(self, username):
        app = App.get_running_app()
        app.set_user(username)
        self.list.remove_widget(self.sign_in)
        self.list.remove_widget(self.register)

        self.my_trips = OneLineListItem(text="My Trips", id="my_trips", on_press=self.my_trips_screen)
        self.list.add_widget(self.my_trips)

        self.sign_out = OneLineListItem(text="Sign Out", id="sign_out", on_press=self.sign_out_screen)
        self.list.add_widget(self.sign_out)

    def my_trips_screen(self, item):
        self.nav_drawer.set_state("close")
        self.screen_manager.current = 'my_trips_view'
        app = App.get_running_app()
        app.view_trips()

    def sign_out_screen(self, item):
        app = App.get_running_app()
        self.list.add_widget(self.sign_in, 4)
        self.list.add_widget(self.register, 4)
        self.list.remove_widget(self.my_trips)
        self.list.remove_widget(self.sign_out)
        app.log_out()


class MainApp(MDApp):
    conn = None
    cur = None
    search_menu = None
    username = None
    map_screen = MapScreen()
    route_maker_screen = RouteMakerScreen()
    my_trips_screen = MyTripsScreen()
    trip_viewer = TripViewer()
    screen_manager = ScreenManagement()
    screen_manager.add_widget(map_screen)
    screen_manager.add_widget(route_maker_screen)
    screen_manager.add_widget(my_trips_screen)

    def on_start(self):
        # GPS init
        GPSHelper().run()

        # Database init
        self.conn = sqlite3.connect("travel_planner.db")
        self.cur = self.conn.cursor()

        # Search Menu init
        self.search_menu = SearchPopupMenu()

    def set_user(self, user):
        self.username = user
        print("Logged in as", self.username)

    def log_out(self):
        print("User", self.username, "has logged out")
        self.username = ""

    def view_trips(self):
        self.trip_viewer.get_trips()


if __name__ == '__main__':
    MainApp().run()
