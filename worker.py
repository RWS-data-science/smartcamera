import os
import time
from skimage import io
import random
import keras


from lees_gps import get_location

#start gps deamon
os.system('sudo gpsd -n /dev/ttyS0 -F /var/run/gpsd.sock')

#load the model
model = keras.models.load_model('model')

while True:
    print('doing one batch of work')
    
    #get time
    t = time.localtime()
    time_string = str(t.tm_year) + '-' + str(t.tm_yday) + '-' + str(t.tm_hour) + '-' + str(t.tm_min) + '-' + str(t.tm_sec)
    
    #get photo
    file_name_image = 'test.jpg'
    command = 'raspistill -o ' + file_name_image + ' -w 1024 -h 1024 --nopreview -t 2000'
    os.system(command)
    photo = io.imread(file_name_image)
    
    #get location
    location = get_location()
    location_string = str(location)
    
    #apply a random condition, later on this conditon is based on model applied to photo
    if(random.randint(0,10) == 5):
        to_sent = [photo, time_string, location_string]
        #Now I would like to sent this information to ESB