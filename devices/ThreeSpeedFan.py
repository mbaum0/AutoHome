"""
This class represents a three speed
fan which is controlled using an
ESP8266 or similar type board. 

@author Michael Baumgarten
@version 7/29/17
"""
import requests


class ThreeSpeedFan(object):
    def __init__(self, name, num, url, speed):
        self.name = name
        self.url = url
        self.speed = speed
        self.num = num

    def turn_off(self):
        self.speed = 0
        url = self.url % 0
        requests.get(url)

    def turn_on(self):
        self.speed = 1
        url = self.url % 1
        requests.get(url)

    def set_speed(self, speed):
        self.speed = speed
        url = self.url % speed
        requests.get(url)
