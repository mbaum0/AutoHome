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








def print_logo():
    print("    ___         __        __  __                  ")
    print("   /   | __  __/ /_____  / / / /___  ____ ___  ___ ")
    print("  / /| |/ / / / __/ __ \\/ /_/ / __ \/ __ `__ \/ _ \\")
    print(" / ___ / /_/ / /_/ /_/ / __  / /_/ / / / / / /  __/")
    print("/_/  |_\__,_/\__/\____/_/ /_/\____/_/ /_/ /_/\___/ ")
    print("___________________________________________________")


def slow_type_string(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(.05)