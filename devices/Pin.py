"""
The Pin class represents a raspberry pi GPIO pin.

@author Michael Baumgarten
@version 6/28/2017
"""
import RPi.GPIO as GPIO


class Pin(object):

    def __init__(self, name, num, on, group):
        self.name = name
        self.num = num
        self.on = on
        self.group = group
        # GPIO.setup(num, GPIO.OUT)

    def turn_off(self):

        self.on = False
        GPIO.output(self.num, GPIO.LOW)

    def turn_on(self):
        self.on = True
        GPIO.output(self.num, GPIO.HIGH)
