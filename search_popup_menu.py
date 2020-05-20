from kivymd.uix.dialog import MDInputDialog
from geopy.geocoders import Nominatim
from kivy.app import App

class SearchPopupMenu(MDInputDialog):
    title = "Enter the desired location:"
    text_button_ok = "Take me there!"

    def __init__(self):
        super().__init__()
        self.size_hint = [.9, .3]
        self.events_callback = self.callback

    def callback(self, *args):
        location = self.text_field.text
        try:
            lat, lon = self.geocode_get_lat_lon(location)
        except ValueError:
            print("Geocoders problem occurred")
            return

        app = App.get_running_app()
        mapview = app.root.ids.mapview
        mapview.center_on(lat, lon)
        mapview.zoom = 10

    def geocode_get_lat_lon(self, location):
        nom = Nominatim()
        loc_data = nom.geocode(location)

        if loc_data.latitude is not None and loc_data.longitude is not None:
            return loc_data.latitude, loc_data.longitude
        raise ValueError
