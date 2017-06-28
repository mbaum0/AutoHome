"""
The Pin class represents a raspberry pi GPIO pin.

@author Michael Baumgarten
@version 6/28/2017
"""
from Device import Device

class Pin(Device):

    def __init__(self, name, num, on):
        self.name = name
        self.num = num
        self.on = on

    def get_name(self):
        return self.name

    def get_num(self):
        return self.num

    def is_on(self):
        return self.on

    def turn_off(self):
        self.on = False

    def turn_on(self):
        self.on = True
