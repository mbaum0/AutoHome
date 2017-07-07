"""
AutoHomeClient presents the user with an interface to interact 
with AutoHome devices. The client makes RESTful HTTP calls to
the server to get and change device statuses

@author Michael Baumgarten
@version 6/30/17
"""
import requests
import os
import time
import sys
from platform import system as system_name


def slow_type_string(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(.05)
    print()


def clear_screen():
    print(chr(27) + "[2J")


def print_logo():
    print("    ___         __        __  __                  ")
    print("   /   | __  __/ /_____  / / / /___  ____ ___  ___ ")
    print("  / /| |/ / / / __/ __ \\/ /_/ / __ \/ __ `__ \/ _ \\")
    print(" / ___ / /_/ / /_/ /_/ / __  / /_/ / / / / / /  __/")
    print("/_/  |_\__,_/\__/\____/_/ /_/\____/_/ /_/ /_/\___/ ")
    print("___________________________________________________")


def get_input_from_user(string, low_range, high_range):
    """
    get numerical input from the user with a specified range
    :param string: message to print
    :param low_range: lower range (inclusive)
    :param high_range: higher range (inclusive)
    :return: the integer input
    """
    while True:
        user_input = input(string)
        try:
            to_int = int(user_input)
            if low_range <= to_int <= high_range:
                return to_int
        except ValueError:
            pass


def get_pin_devices():
    response = requests.get("http://192.168.0.23:5000/pin")
    return response.json()


def get_hue_color_devices():
    response = requests.get("http://192.168.0.23:5000/hue")
    return response.json()


def main_menu():
    print_logo()
    slow_type_string("Welcome! Please select an option below to get started")
    print("(1) view installed devices")
    print("(2) view dashboard")
    print("(3) view AutoHome information")
    selection = get_input_from_user("selection: ", 1, 3)
    options = {1 : view_devices,
               2 : view_dashboard,
               3 : view_info}

    options[selection]()


def view_devices():
    hue_color_lights = get_hue_color_devices()
    gpio_pins = get_pin_devices()

    clear_screen()
    print_logo()
    print("Hue Color Lights:")
    print("_________________")
    for light in hue_color_lights:
        print("name: " + light.name)
        print("id: " + light.num)
        print("xy: [" + light.x+","+light.y+"]")
        print("bri: " + light.brightness)
        print("on: " + light.on)
        print("group: " + light.group)


def view_dashboard():
    pass


def view_info():
    pass


main_menu()
# TODO INCOMPLETE







