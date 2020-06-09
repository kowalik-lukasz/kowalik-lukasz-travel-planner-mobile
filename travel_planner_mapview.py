from kivy.garden.mapview import MapView
from kivy.garden.mapview import MapLayer
from kivy.clock import Clock
from kivy.app import App
from poi_marker import POIMarker
from user_route_marker import UserRouteMarker
from kivymd.uix.label import MDLabel
import requests
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget
from kivymd.uix.button import MDFlatButton


# Properties of the below class in travel_planner_mapview.kv
class TravelPlannerMapView(MapView):
    getting_markers_timer = None
    poi_names = []  # A list to store markers currently displayed on the screen in order not to duplicate them
    active_poi_widgets = []
    active_user_marker_widgets = []

    def cancel_timer(self):
        try:
            self.getting_markers_timer.cancel()
        except:
            pass

    def start_getting_markers_in_fov(self):
        # After one second of users immobility start displaying markers in his fov provided that the zoom in no less
        # than 6.

        self.getting_markers_timer = Clock.schedule_once(self.get_markers_in_fov, 1)
        print(self.zoom)

    def get_markers_in_fov(self, *args):
        min_lat, min_lon, max_lat, max_lon = self.get_bbox()
        bounds = {'min_lat': min_lat, 'min_lon': min_lon, 'max_lat': max_lat, 'max_lon': max_lon, 'mobile': 'true'}
        r = requests.get('http://127.0.0.1:8000/planner/poi/', params=bounds)
        decoded_response = r.json()
        for key, value in decoded_response.items():
            name = value['poi_name']
            if name in self.poi_names:
                continue
            else:
                self.add_poi_marker(value)

    def add_poi_marker(self, poi):
        poi_name = poi['poi_name']
        lat, lon = poi['latitude'], poi['longitude']
        self.poi_names.append(poi_name)
        marker = POIMarker(lat=lat, lon=lon)
        marker.poi_data = poi
        self.add_widget(marker)
        self.active_poi_widgets.append(marker)

    def delete_poi_markers(self):
        for marker in self.active_poi_widgets:
            self.remove_widget(marker)
        self.active_poi_widgets.clear()
        self.poi_names.clear()

    def print_user_route(self, user_route_data):
        # delete previous route
        if self.active_user_marker_widgets:
            self.delete_user_route()

        i = 0
        for loc in user_route_data:
            marker = UserRouteMarker(lat=loc.latitude, lon=loc.longitude, position=i)
            marker.route_data, marker.position = user_route_data, i
            info = i
            label = MDLabel(text=str(info), halign="center", valign="top")
            i += 1
            marker.add_widget(label)

            self.add_widget(marker)
            self.active_user_marker_widgets.append(marker)

    def delete_user_route(self):
        for marker in self.active_user_marker_widgets:
            self.remove_widget(marker)
        self.active_user_marker_widgets.clear()
