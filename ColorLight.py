"""
The ColorLight class represents a phillips hue
color bulb.

@author Michael Baumgarten
@version 6/28/2017

"""
import math


class ColorLight(object):
    def __init__(self, name, x, y, brightness, on):
        self.name = name
        self.x = x
        self.y = y
        self.brightness = brightness
        self.on = on

    def get_name(self):
        return self.name

    def is_on(self):
        return self.on

    def turn_on(self):
        self.on = True

    def turn_off(self):
        self.on = False

    def set_brightness(self, value):
        self.brightness = value

    def get_brightness(self):
        return self.brightness

    def set_x(self, value):
        self.x = value

    def set_y(self, value):
        self.y = value

    def set_xy_by_rbg(self, r, g, b):
        xy = convert_rgb_to_xy(r, g, b)

        self.x = xy[0]
        self.y = xy[1]


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
