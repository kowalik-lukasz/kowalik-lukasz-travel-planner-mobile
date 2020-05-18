import kivy
import sqlite3

kivy.require("1.11.1")

from kivymd.app import MDApp
from travel_planner_mapview import TravelPlannerMapView


class MainApp(MDApp):
    conn = None
    cur = None

    def on_start(self):
        # GPS init

        # Database init
        self.conn = sqlite3.connect("travel_planner.db")
        self.cur = self.conn.cursor()

if __name__ == '__main__':
    MainApp().run()
