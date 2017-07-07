"""
Device is an abstract class that represents a
device used by AutoHome. All devices should
implement the methods described below

@author Michael Baumgarten
@version 6/28/17
"""

from abc import ABC, abstractmethod


class Device(ABC):

    @abstractmethod
    def turn_on(self):
        raise NotImplementedError

    @abstractmethod
    def turn_off(self):
        raise NotImplementedError
