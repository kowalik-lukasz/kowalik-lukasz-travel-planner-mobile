import kivy
import sqlite3
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from travel_planner_mapview import TravelPlannerMapView
from gps_helper import GPSHelper
from search_popup_menu import SearchPopupMenu
from kivy.properties import ObjectProperty
from login_popup import LogInPopup
from route_maker import RouteMaker
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager

kivy.require("1.11.1")


class ScreenManagement(ScreenManager):
    pass


class MapScreen(Screen):
    def switch(self, screen):
        self.screen_manager.current = screen


class RouteMakerScreen(Screen):
    def switch(self, screen):
        self.screen_manager.current = screen


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class MainApp(MDApp):
    conn = None
    cur = None
    search_menu = None
    username = None
    map_screen = MapScreen()
    route_maker_screen = RouteMakerScreen()
    screen_manager = ScreenManagement()
    screen_manager.add_widget(map_screen)
    screen_manager.add_widget(route_maker_screen)

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
