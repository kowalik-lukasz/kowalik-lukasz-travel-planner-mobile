from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivy.properties import ObjectProperty
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

    # Check user input integrity
    def route_input_check(self):

        # Check if the user provided the system with the starting point and endpoint
        if not self.starting_point.text or not self.endpoint.text:
            # error popup
            print("Lack of starting point or endpoint")
            return

        # Check if the midpoints' input is in correct format
        if not re.search("^[0-9a-zA-Z\s-]*(,[0-9a-zA-Z\s-]+)*$", self.midpoints.text):
            # error popup
            print("Incorrect data format")
            return

        travel_locations = get_location_data(self.starting_point, self.midpoints, self.endpoint)

        not_found = []
        for location in travel_locations:
            if location is None:
                not_found.append(location)

        if not_found:
            # error popup, print not found locations
            print("Not found all of the given locations")
            return

        time.sleep(1)
        # Communication with django server
        # app = App.get_running_app()
        # username = app.username
        # print(username)
        # route = {'Start_point': self.starting_point.text, 'Mid_points': self.midpoints.text,
        #          'End_point': self.endpoint, 'mobile': 'true', 'user': username}
        # r = requests.post('http://127.0.0.1:8000/planner/plan_journey/', data=route)
        # print(r)

        print("Done")
