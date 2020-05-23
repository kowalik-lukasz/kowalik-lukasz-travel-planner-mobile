import kivy

kivy.require("1.11.1")

import sqlite3
from kivymd.app import MDApp
from travel_planner_mapview import TravelPlannerMapView
from gps_helper import GPSHelper
from search_popup_menu import SearchPopupMenu


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
