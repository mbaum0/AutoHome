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
import json
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
    clear_screen()
    print_logo()
    # slow_type_string("Welcome! Please select an option below to get started")
    print("(1) view installed devices")
    print("(2) view dashboard")
    print("(3) view AutoHome information")
    selection = get_input_from_user("selection: ", 1, 3)
    options = {1: view_devices,
               2: view_dashboard,
               3: view_info}

    options[selection]()


def view_devices():
    hue_color_lights = get_hue_color_devices()
    gpio_pins = get_pin_devices()

    clear_screen()
    print_logo()
    print()
    print("------------------------")
    print("Hue Color Lights:")
    for light in hue_color_lights:
        print("------------------------")
        print("name: " + light['name'])
        print("id: " + str(light['num']))
        print("xy: [" + str(light['x']) + "," + str(light['y']) + "]")
        print("bri: " + str(light['brightness']))
        print("on: " + str(light['on']))
        print("group: " + light['group'])

    print()
    print("------------------------")
    print("GPIO Pin Devices:")
    for pin in gpio_pins:
        print("------------------------")
        print("name: " + pin['name'])
        print("id: " + str(pin['num']))
        print("on: " + str(pin['on']))
        print("group: " + pin['group'])

    input("press any key to return")
    main_menu()


def view_dashboard():
    clear_screen()
    print("-------------------------------------------------devices------------------------------------------------")
    hue_lights = get_hue_color_devices()
    gpio_pins = get_pin_devices()
    for hue in hue_lights:
        print("(hue) | ", end="")
        print("name: %s | " % hue['name'], end="")
        print("on: %d | " % hue['on'], end="")
        print("id: %d | " % hue['num'], end="")
        print("bri : %d | " % hue['brightness'], end="")
        print("sat : %d | " % hue['saturation'], end="")
        print("group: %s | " % hue['group'], end="")
        print("xy : [%f,%f]" % (hue['x'], hue['y']))

    print()
    for pin in gpio_pins:
        print("(pin) | ", end="")
        print("name: %s | " % pin['name'], end="")
        print("on: %d | " % pin['on'], end="")
        print("id: %d | " % pin['num'], end="")
        print("group: %s " % hue['group'])

    print()
    print("---------------------------------------------enter command---------------------------------------------")
    command = ""
    while command != "exit":
        command = input(":  ")
        print("\r")
        command_args = command.split()

        dev_type = command_args[0]
        dev_state = command_args[1]
        dev_val = str(command_args[2])

        try:
            if dev_val.find('.') == 1:
                dev_val = float(dev_val)
                data = """{"%s" : %f}""" % (dev_state, dev_val)
            else:
                dev_val = int(dev_val)
                data = """{"%s" : %d}""" % (dev_state, dev_val)

            for dev_id in command_args[3:]:
                dev_id = int(dev_id)
                url = "http://192.168.0.23:5000/%s/%d" % (dev_type, dev_id)
                headers = {'content-type': 'application/json'}
                response = requests.put(url, data=data, headers=headers)

                if response.status_code == 404:
                    print("error processing command. please check syntax")
        except ValueError:
            print("error processing command. please check syntax")


    sys.stdout.write("\r")
    sys.stdout.flush()
    main_menu()


def view_info():
    pass


main_menu()
# TODO INCOMPLETE
