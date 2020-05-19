import math
from kivy.garden.mapview import MapView
from kivy.clock import Clock
from kivy.app import App
from poi_marker import POIMarker


# Properties of the below class in travel_planner_mapview.kv
class TravelPlannerMapView(MapView):
    getting_markers_timer = None
    poi_names = []  # A list to store markers currently displayed on the screen in order not to duplicate them

    def start_getting_markers_in_fov(self):
        # After one second of users immobility start displaying markers in his fov provided that the zoom in no less
        # than 6.
        try:
            self.getting_markers_timer.cancel()
        except AttributeError:
            pass

        self.getting_markers_timer = Clock.schedule_once(self.get_markers_in_fov, 1)

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
        self.poi_names.append(poi_name)
        lat, lon = poi[1], poi[2]
        marker = POIMarker(lat=lat, lon=lon)
        marker.poi_data = poi
        self.add_widget(marker)
