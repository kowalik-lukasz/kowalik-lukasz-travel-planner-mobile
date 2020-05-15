import kivy

kivy.require('1.11.1')

from kivy.app import App
from kivy.garden.mapview import MapView


class MapViewApp(App):
    def build(self):
        return MapView(zoom=11, lat=50.6394, lon=3.057)


if __name__ == '__main__':
    MapViewApp().run()
