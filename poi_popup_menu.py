import sqlite3
from kivymd.uix.dialog import ListMDDialog


class POIPopupMenu(ListMDDialog):
    def __init__(self, poi_data):
        super().__init__()
        self.poi_data = poi_data
        headers = ['poi_name', 'latitude', 'longitude']
        for i in range(len(headers)):
            attr_name = headers[i]
            attr_val = str(poi_data[headers[i]])
            setattr(self, attr_name, attr_val)
