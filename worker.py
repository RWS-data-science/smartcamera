
# Worker process for smartcam devices

import base64
import json
import logging
import multiprocessing as mp
import os
import random
import shutil
import time

###

os.environ['KERAS_BACKEND'] = 'theano'

import keras
import numpy as np
import requests
import serial
import pynmea2

try:
    from scipy.misc import imread # deprecated
except:
    from scipy.ndimage import imread

###

IMAGE_FILEPATH = './tmp/image.jpg'
MODEL_FILEPATH = 'tiny_yolo.h5'
GPS_DEVICEPORT = '/dev/tty50'

###

def get_gps_location(ser):
    if not ser: return('no gps device')

    for _ in range(100):
        data = ser.readline().decode('utf-8')
        if data.startswith('$GPRMC'):
            msg = pynmea2.parse(data)
            return ("%s %s %s %s %f" %
                    (msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.spd_over_grnd))
    return('no gps fix')

###

def run(cam_id=0):
    logger = logging.getLogger()
    logger.info("Starting Worker process %d" % mp.current_process().pid)

    try:
        logger.debug("Running keras v%s" % (keras.__version__))
        logger.debug('Loading keras model..')
        model = keras.models.load_model(MODEL_FILEPATH)
    except Exception as e:
        logger.error(e)

    try:
        ser = serial.Serial('/dev/ttyS0', 9600)
    except serial.serialutil.SerialException:
        ser = None
        logger.error('unable to initialise gps device')

    try:
        with open('/etc/esb_url') as fh:
            esb_url = fh.readline().rstrip()
    except Exception:
        logger.error('unable to read esb target url')
        esb_url = 'http://127.0.0.1'

    ###

    while True:
        logger.debug('worker : starting loop')

        # get time
        t = time.localtime()
        time_string = "%d-%d-%d-%d-%d" % (t.tm_year, t.tm_yday, t.tm_hour, t.tm_min, t.tm_sec)

        # get photo
        if not shutil.which('raspistill'):
            logger.error('worker : raspistill utility not found')
            #sys.exit(1)

        logger.debug('worker : taking photo')
        cmd = "raspistill -o %s -w 416 -h 416 --nopreview -t 2000" % IMAGE_FILEPATH
        os.system(cmd)
        logger.debug('worker : reading photo')
        photo = imread(IMAGE_FILEPATH)
        photo = np.expand_dims(photo, axis=0)

        # get location
        logger.debug('worker : get location')
        location_string = get_gps_location(ser)

        # NOTE: dummy array to match model layout:
        dummy = np.zeros([1, 1, 1, 1, 10, 4])

        logger.debug('worker : make prediction')
        prediction = model.predict([photo, dummy])

        # apply a random condition, later on this conditon is based on model applied to photo
        if random.randint(0, 10) == 5:
            logger.debug('worker : selected')
            with open(IMAGE_FILEPATH, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

            # information to be sent
            to_sent = {'photo': encoded_string.decode('ascii'),
                       'time': time_string,
                       'location': location_string,
                       'filename': "%s_%s_%s" % (cam_id, time_string, location_string)
                      }

            # construct json
            logger.debug('worker : sending json msg')
            to_sent = json.dumps(to_sent)

            # sent json:
            try:
                # a message is approximately 180kb, so even when connection
                # falls back to gsm/2g speed at @ 14.4 kbps upload, a timeout
                # of a minute should suffice
                res = requests.post(esb_url, json=to_sent, timeout=60)
                if res.status_code == 200:
                    logger.debug('succesfully sent data')
            except Exception as e:
                logger.error(e)

#run()
