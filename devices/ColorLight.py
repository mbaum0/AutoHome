"""
The ColorLight class represents a phillips hue
color bulb.

@author Michael Baumgarten
@version 6/28/2017

"""
from devices.Device import Device
import requests

HUE_REST_URL = "http://192.168.0.2/api/Qryu0vLk1-aRsaDfnXY8puTr1yiN4TylHMlB7Qql/lights/%d/state"


class ColorLight(object):

    def __init__(self, name, num, x, y, brightness, on, saturation):
        self.name = name
        self.num = num
        self.x = x
        self.y = y
        self.brightness = brightness
        self.on = on
        self.saturation = saturation

    def turn_off(self):
        self.on = False
        url = (HUE_REST_URL % self.num)
        body = "{\"on\":false}"
        response = requests.put(url, data=body)

    def turn_on(self):
        self.on = True
        url = (HUE_REST_URL % self.num)
        body = "{\"on\":true}"
        response = requests.put(url, data=body)

    def set_color(self, x, y):
        self.y = y
        self.x = x
        url = (HUE_REST_URL % self.num)
        body = "{\"xy\":[%f,%f]}" % (x, y)
        response = requests.put(url, data=body)

    def set_brightness(self, val):
        self.brightness = val
        url = (HUE_REST_URL % self.num)
        body = "{\"bri\":%d}" % val
        response = requests.put(url, data=body)

    def set_saturation(self, val):
        self.saturation = val
        url = (HUE_REST_URL % self.num)
        body = "{\"sat\":%d}" % val
        response = requests.put(url, data=body)







