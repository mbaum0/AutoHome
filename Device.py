"""
Device is an abstract class that represents a
device used by AutoHome. All devices should
implement the methods described below

@author Michael Baumgarten
@version 6/28/17
"""

class Device:
    def get_name(self):
        raise NotImplementedError

    def is_on(self):
        raise NotImplementedError

    def turn_on(self):
        raise NotImplementedError

    def turn_off(self):
        raise NotImplementedError