import os
from kivy.garden.mapview import MapMarkerPopup


class UserRouteMarker(MapMarkerPopup):
    source = os.path.join("img", "user_route_icon.png")
