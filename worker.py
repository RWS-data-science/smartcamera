
# Worker process for smartcam devices

import base64
import json
import multiprocessing as mp
import os
<<<<<<< HEAD
os.chdir('/home/daniel/projecten/smartcamera')

import time
from scipy.misc import imread
import random
import keras
import json
import base64
import numpy as np
import random
import time

# force keras backend:
os.environ['KERAS_BACKEND'] = 'theano'
import keras
from scipy.ndimage import imread

from lees_gps import get_location

#start gps deamon
os.system('sudo gpsd -n /dev/ttyS0 -F /var/run/gpsd.sock')

#load the model
model = keras.models.load_model('yolo.h5')

while True:
    print('doing one batch of work')
    
    #get time
    t = time.localtime()
    time_string = str(t.tm_year) + '-' + str(t.tm_yday) + '-' + str(t.tm_hour) + '-' + str(t.tm_min) + '-' + str(t.tm_sec)
    
    #get photo
    file_name_image = 'test.jpg'
    command = 'raspistill -o ' + file_name_image + ' -w 1024 -h 1024 --nopreview -t 2000'
    os.system(command)
    photo = imread(file_name_image)
    photo = np.expand_dims(photo, axis = 0)
    
    #get location
    location = get_location()
    location_string = str(location)
    
    prediction = model.predict(photo)
    
    #apply a random condition, later on this conditon is based on model applied to photo
    if(random.randint(0,10) == 5):
        with open(file_name_image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        #information to be sent
        to_sent = {'photo': encoded_string, 'time': time_string, 'location':location_string, 'filename': pi_id + '_' + time_string + '_' + location_string }
        #construct json
        to_sent = json.dumps(to_sent)

def run(cam_id, logger):
    logger.info("Starting Worker process #%d" % mp.current_process().pid)
    while True:
        #get time
        t = time.localtime()
        time_string = str(t.tm_year) + '-' + str(t.tm_yday) + '-' + str(t.tm_hour) + '-' + str(t.tm_min) + '-' + str(t.tm_sec)

        #get photo
        file_name_image = 'test.jpg'
        command = 'raspistill -o ' + file_name_image + ' -w 1024 -h 1024 --nopreview -t 2000'
        os.system(command)
        photo = imread(file_name_image)

        #get location
        location_string = str(get_location)

        #apply a random condition, later on this conditon is based on model applied to photo
        if random.randint(0, 10) == 5:
            with open(file_name_image, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            #information to be sent
            to_sent = {'photo': encoded_string,
                       'time': time_string,
                       'location':location_string,
                       'filename': "%s_%s_%s" % (cam_id, time_string, location_string)
                      }

            #construct json
            to_sent = json.dumps(to_sent)
