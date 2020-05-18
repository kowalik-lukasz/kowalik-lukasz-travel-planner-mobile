import math
from kivy.garden.mapview import MapView
from kivy.clock import Clock
from kivy.app import App


# Properties of the below class in travel_planner_mapview.kv
class TravelPlannerMapView(MapView):
    getting_markers_timer = None

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
        query = "SELECT * FROM poi WHERE latitude_radian > %s AND latitude_radian <%s AND longitude_radian > %s AND " \
                "longitude_radian <%s" % (min_lat, max_lat, min_lon, max_lon)
        app.cur.execute(query)
        poi = app.cur.fetchall()
        print(poi)
