"""
Utils contains various functions used for setup
and configuration.

@author Michael Baumgarten
@version 6/29/17

"""
import logging
import math
import sqlite3
from sqlite3 import OperationalError

import RPi.GPIO as GPIO
from devices.ColorLight import ColorLight

from devices.Pin import Pin

# configurations
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def gpio_init():
    """
    initializes the gpio header on a raspberry pi
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


def db_init():
    """
    run database initialization script
    """
    connection = sqlite3.connect("autohome.db")
    cursor = connection.cursor()
    update_script = open('database_init.sql', 'r')
    sql_file = update_script.read()
    update_script.close()

    sql_commands = sql_file.split(";")

    for command in sql_commands:
        try:
            cursor.execute(command)
            logger.info("SQL EXECUTE: " + command)
        except OperationalError as e:
            logger.error("ERROR EXECUTING SQL COMMAND: %s" % e)

    connection.commit()


def get_pin_db_devices():
    """
    retrieves a list of pin devices that are currently configured
    in the database
    :return: list of pin devices
    """

    pins_get_devices = "SELECT * FROM pins"
    connection = sqlite3.connect("autohome.db")
    cursor = connection.cursor()

    cursor.execute(pins_get_devices)
    connection.commit()
    pin_devs = cursor.fetchall()
    pin_objs = []

    for dev in pin_devs:
        pin_objs.append(Pin(dev[1], dev[0], dev[2], dev[3]))

    return pin_objs


def get_hue_color_db_devices():
    """
    retrieves a list of hue_color devices that are currently configured
    in the database
    :return: list of hue color devices
    """

    hue_colors_get_devices = "SELECT * FROM hue_colors"
    connection = sqlite3.connect("autohome.db")
    cursor = connection.cursor()

    cursor.execute(hue_colors_get_devices)
    connection.commit()
    hue_color_devs = cursor.fetchall()
    light_objs = []

    for dev in hue_color_devs:
        light_objs.append(ColorLight(dev[1], dev[0], dev[4], dev[5], dev[3], dev[2], dev[6], dev[7]))

    return light_objs


def convert_rgb_to_xy(red, green, blue):
    """
    converts red green and blue values to 
    phillips hue xy convention values
    :param red: red value 0-254
    :param green: green value 0-254
    :param blue: blue value 0-254
    :return: tuple (x,y)
    """
    if red > .04045:
        red = math.pow(((red + .055) / (1.0 + .055)), 2.4)
    else:
        red = (red / 12.92)

    if green > .04045:
        green = math.pow(((green + .055) / (1.0 + .055)), 2.4)
    else:
        green = (green / 12.92)

    if blue > .04045:
        blue = math.pow(((blue + .055) / (1.0 + .055)), 2.4)
    else:
        blue = (blue / 12.92)

    x = red * .664511 + green * .154324 + blue * .162028

    y = red * .283881 + green * .668433 + blue * .047685

    z = red * .000088 + green * .072310 + blue * .986039

    fx = x / (x + y + z)
    fy = y / (x + y + z)

    if math.isnan(fx):
        fx = 0.0

    if math.isnan(fy):
        fy = 0.0

    return round(fx, 4), round(fy, 4)
