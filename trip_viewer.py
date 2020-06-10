from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, OneLineListItem
from kivy.app import App
from functools import partial
from route_maker import get_location_data
import requests


class TripViewer(FloatLayout):
    trip_list = ObjectProperty(MDList)
    route_list = []
    md_item_list = []

    def get_trips(self):

        app = App.get_running_app()

        username = app.username
        r = requests.get('http://127.0.0.1:8000/planner/user_profile_page/',
                         params={'mobile': 'true', 'username': username})
        decoded_response = r.json()

        for element in self.md_item_list:
            app.root.ids.trip_viewer.ids.trip_list.remove_widget(element)

        self.md_item_list = []

        for key, value in decoded_response.items():
            name = value['Route']
            route = name.strip('][').split(', ')
            clean_route = []

            for elements in route:
                clean_route.append(elements[1:-1])

            listName = str(clean_route[0])
            for i in range(len(clean_route)):
                if i == 0:
                    continue
                listName += "," + str(clean_route[i])
            listItem = OneLineListItem(text=listName)
            self.md_item_list.append(listItem)
            listItem.bind(on_press=partial(self.map_route, clean_route))
            app.root.ids.trip_viewer.ids.trip_list.add_widget(listItem, 1)

    def map_route(self, *args):
        print(args)
        app = App.get_running_app()

        route = args[0]
        starting_point = route.pop(0)
        ending_point = route.pop(len(route)-1)
        mid_points = route

        locations = get_location_data(starting_point, mid_points, ending_point, "from_trip_viewer")

        app.root.ids.screen_manager.current = "main_view"

        app.root.ids.mapview.lat = locations[0].latitude
        app.root.ids.mapview.lon = locations[0].longitude
        app.root.ids.mapview.zoom = 10
        app.root.ids.mapview.print_user_route(locations)
