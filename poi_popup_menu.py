import sqlite3
from kivymd.uix.dialog import ListMDDialog


class POIPopupMenu(ListMDDialog):
    def __init__(self, poi_data):
        super().__init__()

        self.poi_data = poi_data
        conn = sqlite3.connect("travel_planner.db")
        cur = conn.execute("SELECT * FROM poi")
        headers = [description[0] for description in cur.description]

        unused_headers = 4
        for i in range(len(headers) - unused_headers):
            print(headers[i])
            print(poi_data[i])
            attr_name = headers[i]
            attr_val = str(poi_data[i])
            setattr(self, attr_name, attr_val)