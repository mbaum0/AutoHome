"""
ServiceProvider runs the Flask application and creates a RESTful services
for accesses and manipulating devices

@author Michael Baumgarten
@version 6/29/17
"""
from flask import Flask
from flask import abort
from flask import request
import json
from Utils import get_hue_color_db_devices, get_pin_db_devices, gpio_init
import logging

# configurations
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

    data = request.get_json()[0]
    status = data['on']
    if status == 0:
        pins[0].turn_off()
    else:
        pins[0].turn_on()

    return json.dumps(pins[0].__dict__)


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

"""
************************* INITIALIZATION FUNCTIONS *************************
"""


def main():
    logger.debug("INITIALIZING")
    gpio_init()
    init_devices()
    logger.debug("LAUNCHING FLASK PROCESS")
    app.run(debug=True, host='192.168.0.23')

if __name__ == '__main__':
    main()



