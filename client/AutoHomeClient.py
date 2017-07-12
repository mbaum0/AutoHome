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

SERVER_URL = "http://192.168.0.75:5000"

COMMANDS = ["colors"]


def slow_type_string(msg):
    for letter in msg:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(.025)
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
    response = requests.get(SERVER_URL+"/pin")
    return response.json()


def get_hue_color_devices():
    response = requests.get(SERVER_URL+"/hue")
    return response.json()


def main_menu():
    clear_screen()
    print_logo()
    slow_type_string("Welcome! Please select an option below.")
    print("(1) view installed devices")
    print("(2) adjust devices")
    print("(3) view AutoHome information")
    selection = get_input_from_user("selection: ", 1, 3)
    options = {1: view_devices,
               2: view_commands,
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

    print()
    input("press any key to return")
    main_menu()


def view_commands():
    command = ""
    error = False
    while command != "exit":
        clear_screen()
        print_logo()
        print(' DEVICES '.center(120, '*'))
        hue_lights = get_hue_color_devices()
        gpio_pins = get_pin_devices()
        for hue in hue_lights:
            print("(hue) | ", end="")
            print("name: %s | " % hue['name'], end="")
            print("on: %d | " % hue['on'], end="")
            print("id: %d | " % hue['num'], end="")
            print("bri: %d | " % hue['brightness'], end="")
            print("sat: %d | " % hue['saturation'], end="")
            print("group: %s | " % hue['group'], end="")
            print("xy: [%f,%f]" % (hue['x'], hue['y']))

        print()
        for pin in gpio_pins:
            print("(pin) | ", end="")
            print("name: %s | " % pin['name'], end="")
            print("on: %d | " % pin['on'], end="")
            print("id: %d | " % pin['num'], end="")
            print("group: %s " % hue['group'])

        print()

        print(' COLORS '.center(120, '*'))

        colors = get_colors()
        i = 0
        for color in colors:
            print(color + " ", end=" ")
            i += len(color)
            if i >= 85:
                print()
                i = 0

        print()

        print(' ENTER COMMAND '.center(120, '*'))
        if error:
            print("error processing command. please check syntax")
            error = False
        command = input(":  ")
        print("\r")
        command_args = command.split()

        if len(command_args) < 2:
            error = True
        else:
            if command_args[0] == 'cmd':
                if command_args[1] in COMMANDS:
                    process_command(command_args[1])
                else:
                    error = True
            else:
                dev_type = command_args[0]
                dev_state = fix_dev_state_input(command_args[1])
                dev_val = str(command_args[2])

                try:
                    data = ''
                    if is_float(dev_val):
                        dev_val = float(dev_val)
                        data = """{"%s" : %f}""" % (dev_state, dev_val)
                    elif is_int(dev_val):
                        dev_val = int(dev_val)
                        data = """{"%s" : %d}""" % (dev_state, dev_val)
                    elif isinstance(dev_val, str):
                        data = """{"%s" : "%s"}""" % (dev_state, dev_val)

                    for dev_id in command_args[3:]:
                        dev_id = int(dev_id)
                        url = SERVER_URL+"/%s/%d" % (dev_type, int(dev_id))
                        headers = {'content-type': 'application/json'}
                        response = requests.put(url, data=data, headers=headers)

                        if response.status_code == 404:
                            error = True
                except ValueError:
                    error = True

        sys.stdout.write("\r")
        sys.stdout.flush()
    main_menu()


def view_info():
    clear_screen()
    print_logo()
    print()
    print("AutoHome is a client-server based IOT service. The server is meant to be run on a small computer")
    print("i.e a Raspberry Pi. The server manages processing requests and manipulating devices based on ")
    print("queries. The server is set up in a RESTful manner where it handles HTTP requests with JSON data")
    print("in order to determine which devices to look at and how to change them.")
    print()
    print("AutoHome is originally made to work with the rPi GPIO header and Phillips Hue bulbs. As time goes")
    print("on I plan to add support for music playback (vlc) and creating some kind of rpi/python interface")
    print("to allow new everyday devices to be added to AutoHome.")
    print()
    print("Created By Michael Baumgarten - Summer 2017")
    print()
    input("Press any key to go back")
    main_menu()


def fix_dev_state_input(state):
    """
    allows users to use shorter notations for commands
    :param state: user shorthand input
    :return: corrected input
    """
    if state == 'sat':
        return 'saturation'
    if state == 'bri':
        return 'brightness'
    return state


def is_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def is_float(val):

    if '.' in val:
        try:
            float(val)
            return True
        except ValueError:
            return False
    return False


def process_command(cmd):
    if cmd == "colors":
        print("Colors Go Here")


def get_colors():
    url = SERVER_URL+"/hue/colors"
    response = requests.get(url)
    content = response.json()
    color_list = []
    for key in content:
        color_list.append(key)

    return color_list



main_menu()
# TODO INCOMPLETE
