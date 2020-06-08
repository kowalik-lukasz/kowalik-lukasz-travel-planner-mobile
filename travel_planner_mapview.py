from kivy.garden.mapview import MapView
from kivy.garden.mapview import MapLayer
from kivy.clock import Clock
from kivy.app import App
from poi_marker import POIMarker
from user_route_marker import UserRouteMarker
from kivymd.uix.label import MDLabel
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
        app = App.get_running_app()
        query = "SELECT * FROM poi WHERE latitude > %s AND latitude <%s AND longitude > %s AND longitude <%s" % (
            min_lat, max_lat, min_lon, max_lon)
        app.cur.execute(query)
        pois = app.cur.fetchall()
        print(pois)
        for poi in pois:
            name = poi[0]
            if name in self.poi_names:
                continue
            else:
                self.add_poi_marker(poi)

    def add_poi_marker(self, poi):
        poi_name = poi[0]
        lat, lon = poi[1], poi[2]
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

        i = 1
        for loc in user_route_data:
            marker = UserRouteMarker(lat=loc.latitude, lon=loc.longitude)
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
