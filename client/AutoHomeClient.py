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
    user_input = input(string)
    try:
        to_int = int(user_input)
        if low_range <= to_int <= high_range:
            return to_int
        get_input_from_user(string, low_range, high_range)
    except ValueError:
        get_input_from_user(string, low_range, high_range)


def get_pin_devices():
    response = requests.get("http://192.168.0.23:5000/pin")
    return response.json()


def get_hue_color_devices():
    response = requests.get("http://192.168.0.23:5000/hue")
    return response.json()

# TODO INCOMPLETE







