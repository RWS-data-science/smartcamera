
# Worker process for smartcam devices

import base64
import json
import logging
import multiprocessing as mp
import os
import random
import shutil
import sys
import time

###

os.environ['KERAS_BACKEND'] = 'theano'

import keras
import numpy as np
import serial
import pynmea2

try:
    from scipy.misc import imread # deprecated
except:
    from scipy.ndimage import imread

###

IMAGE_FILEPATH = './tmp/image.jpg'
MODEL_FILEPATH = 'model'
GPS_DEVICEPORT = '/dev/tty50'

###

def get_gps_location(ser):
    if not ser: return('no gps device')

    for i in range(100):
        data = ser.readline().decode('utf-8')
        if data.startswith('$GPRMC'):
            msg = pynmea2.parse(data)
            return (msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.spd_over_grnd)
    return('no gps fix')

###

def run(cam_id=None):
    logger = logging.getLogger()
    logger.info("Starting Worker process %d" % mp.current_process().pid)

    logger.debug('Loading keras model..')
    model = keras.models.load_model('/home/daniel/projecten/smartcamera/tiny_yolo.h5' )

    try:
        ser = serial.Serial('/dev/ttyS0',9600)
    except serial.serialutil.SerialException:
        ser = None
        logger.error('unable to initialise gps device')

    ###

    while True:
        logger.debug('worker : starting loop')

        #get time
        t = time.localtime()
        time_string = "%d-%d-%d-%d-%d" % (t.tm_year, t.tm_yday, t.tm_hour, t.tm_min, t.tm_sec)

        #get photo
        if not shutil.which('raspistill'):
            logger.error('worker : raspistill utility not found')
            sys.exit(1)

        logger.debug('worker : taking photo')
        cmd = "raspistill -o %s -w 1024 -h 1024 --nopreview -t 2000" % IMAGE_FILEPATH
        os.system(cmd)
        logger.debug('worker : reading photo')
        photo = imread(IMAGE_FILEPATH)
        logger.debug('worker : expand dims')
        photo = np.expand_dims(photo, axis=0)

        #get location
        logger.debug('worker : get location')
        location = get_gps_location(ser)
        location_string = str(location)

        logger.debug('worker : make prediction')
        prediction = model.predict(photo)

        #apply a random condition, later on this conditon is based on model applied to photo
        if random.randint(0, 10) == 5:
            logger.debug('worker : selected')
            with open(IMAGE_FILEPATH, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

            #information to be sent
            to_sent = {'photo': encoded_string,
                       'time': time_string,
                       'location': location_string,
                       'filename': "%s_%s_%s" % (cam_id, time_string, location_string)
                      }

            #construct json
            logger.debug('worker : sending json msg')
            to_sent = json.dumps(to_sent)

#run()
