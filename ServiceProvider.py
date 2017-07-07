"""
ServiceProvider runs the Flask application and creates a RESTful services
for accesses and manipulating devices

@author Michael Baumgarten
@version 6/29/17
"""
import json
import logging

from flask import Flask
from flask import abort
import sys
from flask import request
from Utils import get_hue_color_db_devices, get_pin_db_devices, gpio_init, db_init

# configurations
app = Flask(__name__)

LOG_FILENAME = "am.log"
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler(LOG_FILENAME, mode='w')
handler.setFormatter(formatter)
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(screen_handler)

# global vars
HOME_MESSAGE = "It works!"
PIN_DEVICES = []
HUE_COLOR_DEVICES = []

"""
************************* INITIALIZATION *************************
"""


def init_devices():
    """
    fill the device lists with devices
    """
    logger.debug("LOADING PIN DEVICES FROM DATABASE")
    global PIN_DEVICES
    PIN_DEVICES = get_pin_db_devices()

    logger.debug("LOADING HUE COLOR DEVICES FROM DATABASE")
    global HUE_COLOR_DEVICES
    HUE_COLOR_DEVICES = get_hue_color_db_devices()


"""
************************* DEVICE REST SERVICES *************************
"""


@app.route('/')
def home():
    return HOME_MESSAGE


# GPIO DEVICES

@app.route('/pin/<int:num>', methods=['PUT'])
def pin_set(num):
    logger.debug("GOT REQUEST FOR GPIO PIN %d" % num)
    global PIN_DEVICES

    pins = [pin for pin in PIN_DEVICES if pin.num == num]

    if len(pins) == 0:
        abort(404)
    if not request.json:
        abort(404)
    if 'on' in request.json and type(request.json['on']) is not int:
        abort(404)

    data = request.get_json()
    status = data['on']
    if status == 0:
        pins[0].turn_off()
    else:
        pins[0].turn_on()

    return json.dumps(pins[0].__dict__)


@app.route('/pin/group/<string:group>', methods=['PUT'])
def pin_group_set(group):
    logger.debug("GOT REQUEST FOR GPIO PIN GROUP %s" % group)
    global PIN_DEVICES

    pins = [pin for pin in PIN_DEVICES if pin.group == group]

    if len(pins) == 0:
        abort(404)
    if not request.json:
        abort(404)
    if 'on' in request.json and type(request.json['on']) is not int:
        abort(404)

    data = request.get_json()
    if 'on' in request.json:
        if data['on'] == 0:
            for pin in pins:
                pin.turn_off()

        if data['on'] == 1:
            for pin in pins:
                pin.turn_on()

    return json.dumps([pin.__dict__ for pin in pins])


# HUE COLOR DEVICES
@app.route('/hue/<int:num>', methods=['PUT'])
def hue_color_set(num):
    logger.debug("GOT REQUEST FOR HUE COLOR LIGHT %d" % num)
    global HUE_COLOR_DEVICES

    lights = [light for light in HUE_COLOR_DEVICES if light.num == num]

    if len(lights) == 0:
        abort(404)
    if not request.json:
        abort(404)
    if 'on' in request.json and type(request.json['on']) is not int:
        abort(404)
    if 'bri' in request.json and type(request.json['bri']) is not int:
        abort(404)
    if 'x' in request.json and type(request.json['x']) is not float:
        abort(404)
    if 'y' in request.json and type(request.json['y']) is not float:
        abort(404)
    if 'sat' in request.json and type(request.json['sat']) is not int:
        abort(404)

    data = request.get_json()
    if 'on' in request.json:
        if data['on'] == 1:
            lights[0].turn_on()
        else:
            lights[0].turn_off()

    if 'bri' in request.json:
        bright = data['bri']
        lights[0].set_brightness(bright)
    if 'xy' in request.json:
        xy = data['xy']
        lights[0].set_color(xy[0], xy[1])
    if 'sat' in request.json:
        sat = data['sat']
        lights[0].set_saturation(sat)

    return json.dumps(lights[0].__dict__)


@app.route('/hue/group/<string:group>', methods=['PUT'])
def hue_color_group_set(group):
    logger.debug("GOT REQUEST FOR HUE COLOR LIGHT GROUP %s " % group)
    global HUE_COLOR_DEVICES

    lights = [light for light in HUE_COLOR_DEVICES if light.group == group]

    if len(lights) == 0:
        abort(404)
    if not request.json:
        abort(404)
    if 'on' in request.json and type(request.json['on']) is not int:
        abort(404)
    if 'bri' in request.json and type(request.json['bri']) is not int:
        abort(404)
    if 'x' in request.json and type(request.json['x']) is not float:
        abort(404)
    if 'y' in request.json and type(request.json['y']) is not float:
        abort(404)
    if 'sat' in request.json and type(request.json['sat']) is not int:
        abort(404)

    data = request.get_json()
    if 'on' in request.json:
        if data['on'] == 1:
            for light in lights:
                light.turn_on()
        else:
            for light in lights:
                light.turn_off()
    if 'bri' in request.json:
        bright = data['bri']
        for light in lights:
            light.set_brightness(bright)
    if 'xy' in request.json:
        xy = data['xy']
        for light in lights:
            light.set_color(xy[0], xy[1])
    if 'sat' in request.json:
        sat = data['sat']
        for light in lights:
            light.set_saturation(sat)

    return json.dumps([light.__dict__ for light in lights])


"""
************************* INITIALIZATION FUNCTIONS *************************
"""


def main():
    logger.debug("INITIALIZING")
    db_init()
    gpio_init()
    init_devices()
    logger.debug("LAUNCHING FLASK PROCESS")
    app.run(debug=True, host='192.168.0.23')
    logger.debug("SERVER RUNNING")


if __name__ == '__main__':
    main()
