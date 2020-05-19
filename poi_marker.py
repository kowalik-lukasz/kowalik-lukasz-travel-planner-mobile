import os
from kivy.garden.mapview import MapMarkerPopup
from poi_popup_menu import POIPopupMenu


class POIMarker(MapMarkerPopup):
    source = os.path.join("img", "poi_marker.png")
    poi_data = []

    def on_release(self):
        menu = POIPopupMenu(self.poi_data)
        menu.size_hint = [.8, .8]
        menu.open()
