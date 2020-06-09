import os
from kivy.garden.mapview import MapMarkerPopup
from kivymd.uix.dialog_orig import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.app import App


class UserRouteMarker(MapMarkerPopup):
    source = os.path.join("img", "user_route_icon.png")
    route_data = []

    def __init__(self, lat, lon, position):
        super().__init__(lat=lat, lon=lon)
        self.position = position

    def on_release(self):

        previous_button = MDRaisedButton(text="Previous Location", on_release=self.goto_previous_location)
        next_button = MDRaisedButton(text="Next Location", on_release=self.goto_next_location)
        if self.position == 0:
            previous_button.disabled = True
        elif self.position == len(self.route_data) - 1:
            next_button.disabled = True

        popup = MDDialog(title="Route Info", text=f"Which in order: {self.position} \n"
                                                  f"Location info: {self.route_data[self.position].address}",
                         size_hint=[.5, .5], auto_dismiss=True, buttons=[previous_button, next_button])
        previous_button.bind(on_press=popup.dismiss)
        next_button.bind(on_press=popup.dismiss)
        popup.open()
        return

    def goto_previous_location(self, *args):
        app = App.get_running_app()
        app.root.ids.mapview.lat = self.route_data[self.position - 1].latitude
        app.root.ids.mapview.lon = self.route_data[self.position - 1].longitude
        app.root.ids.mapview.zoom = 10

    def goto_next_location(self, *args):
        app = App.get_running_app()
        app.root.ids.mapview.lat = self.route_data[self.position + 1].latitude
        app.root.ids.mapview.lon = self.route_data[self.position + 1].longitude
        app.root.ids.mapview.zoom = 10
