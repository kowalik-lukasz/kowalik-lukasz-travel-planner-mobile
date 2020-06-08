from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivy.properties import ObjectProperty
from kivymd.uix.dialog_orig import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from geopy.geocoders import Nominatim
from kivy.app import App
import threading
import time
import concurrent.futures
import re
import requests


def send_geocode_request(location, nom):
    print('{}: starting with {}'.format(threading.current_thread().name, location))
    result = nom.geocode(location)
    print('{}: done with {}'.format(threading.current_thread().name, result))
    return result


def get_location_data(starting_point, midpoints, endpoint):
    midpoints_list = midpoints.text.split(',')
    travel_locations = [starting_point.text]  # [send_geocode_request(starting_point.text)]
    if midpoints.text:
        print("weszo")
        for location in midpoints_list:
            travel_locations.append(location)
    travel_locations.append(endpoint.text)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        args = ((i, Nominatim(user_agent="travel-planner-app", timeout=20)) for i in travel_locations)
        results = executor.map(lambda p: send_geocode_request(*p), args)
        executor.shutdown(wait=True)
        real_results = list(results)
        print(real_results)

    return real_results


class RouteMaker(MDBoxLayout):
    starting_point = ObjectProperty(None)
    midpoints = ObjectProperty(None)
    endpoint = ObjectProperty(None)
    travel_locations = []

    # Check user input integrity
    def route_input_check(self):

        # Check if the user provided the system with the starting point and endpoint
        if not self.starting_point.text or not self.endpoint.text:
            popup = MDDialog(title="Error", text="Either starting point or endpoint not provided!", size_hint=[.5, .5],
                             auto_dismiss=True)
            popup.open()
            print("Lack of starting point or endpoint")
            return

        # Check if the midpoints' input is in correct format
        if not re.search(r"^[0-9a-ząćęłńóśżźA-ZĄĆĘŁŃÓŚŻŹ\s-]*(,[0-9a-ząćęłńóśżźA-ZĄĆĘŁŃÓŚŻŹ\s-]+)*$",
                         self.midpoints.text):
            popup = MDDialog(title="Error", text="Incorrect data format in 'midpoints' field!", size_hint=[.5, .5],
                             auto_dismiss=True)
            popup.open()
            print("Incorrect data format")
            return

        print(self.midpoints.text)
        self.travel_locations = get_location_data(self.starting_point, self.midpoints, self.endpoint)
        for location in self.travel_locations:
            if location is None:
                popup = MDDialog(title="Error", text="At least one of the provided locations was not found!",
                                 size_hint=[.5, .5], auto_dismiss=True)
                popup.open()
                print("Not found all of the given locations")
                return

        locations_text = ""
        for location in self.travel_locations:
            locations_text += " - " + location.address + "\n"

        no_button = MDFlatButton(text="No")
        yes_button = MDRaisedButton(text="Yes", on_release=self.get_route_from_server)

        popup = MDDialog(title="Confirm Route",
                         text=f"Do the below locations match your expectations:\n{locations_text}",
                         size_hint=[.5, .5], auto_dismiss=True,
                         buttons=[no_button, yes_button])
        no_button.bind(on_press=popup.dismiss)
        yes_button.bind(on_press=popup.dismiss)
        popup.open()
        return

    def get_route_from_server(self, *args):
        # Communication with django server
        app = App.get_running_app()
        username = app.username
        route = {'Start_point': self.starting_point.text, 'Mid_points': self.midpoints.text,
                 'End_point': self.endpoint.text, 'mobile': 'true', 'user': username}
        r = requests.post('http://127.0.0.1:8000/planner/plan_journey/', data=route)
        print(r.text)

        app.root.ids.screen_manager.current = "main_view"
        user_route = r.text.split(',')

        # Sorting self.travel_locations in an order in which user_route is received from the server
        i = 0
        for loc in user_route:
            j = 0
            while j < len(self.travel_locations):
                if loc in self.travel_locations[j].address:
                    self.travel_locations[j], self.travel_locations[i] = self.travel_locations[i], \
                                                                         self.travel_locations[j]
                    break
                j += 1
            i += 1

        app.root.ids.mapview.lat = self.travel_locations[0].latitude
        app.root.ids.mapview.lon = self.travel_locations[0].longitude
        app.root.ids.mapview.zoom = 10
        app.root.ids.mapview.print_user_route(self.travel_locations)
